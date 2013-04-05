from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.db.models import Q


from search.models import Experiment, Gene
from search.forms import QueryDB_SearchForm, GeneEnrichement_SearchForm, DirectTargets_SearchForm
from search._constants import (SPECIES_CHOICES,
                               TF_CHOICES,
                               EXPT_CHOICES,
                               EXPT_WEIGHTS,
                               DIRECT_SEARCH_THRESHOLD)


import settings


import os
import operator
import random
import json
import tablib


def _search(form):
    print form.cleaned_data
    results = Experiment.objects.all()
    row_index = int(form.cleaned_data.pop('row_index'))
    species = None
    if form.cleaned_data['transcription_factor']:
        tfs = json.loads(form.cleaned_data.pop('transcription_factor'))
        results = results.filter(transcription_factor__in=tfs)
    if form.cleaned_data['expt_type']:
        expts = json.loads(form.cleaned_data.pop('expt_type'))
        results = results.filter(expt_type__in=expts)
    if form.cleaned_data['species']:
        species = json.loads(form.cleaned_data.pop('species'))
        results = results.filter(species__in=species)
    if form.cleaned_data['gene']:
        gene = form.cleaned_data.pop('gene')
        if species is not None:
            fnames = [s.lower() for s in species]
        else:
            fnames = [field.name for field in Gene._meta.fields]
            fnames.remove('id')
        if fnames:
            qgroup = reduce(operator.or_,
                            (Q(**{name: gene}) for name in fnames))
            genes = Gene.objects.filter(qgroup)
            results = results.filter(gene__in=genes)

    for key, value in form.cleaned_data.iteritems():
        if value:
            results = results.filter(**{key: value})
    count = results.count()
    return results, count, row_index


def search(request):
    """Search through the experiments for a search term."""
    form = QueryDB_SearchForm(request.POST or None)
    if not form.is_valid():
        return render_to_response("search.html",
                                  {'form': form,
                                   'tf_choices': json.dumps(TF_CHOICES),
                                   'tft_species':json.dumps(SPECIES_CHOICES),
                                   'tft_expt_types':json.dumps(EXPT_CHOICES)},
                                  context_instance=RequestContext(request))

    results, count, row_index = _search(form)
    serialized = _serialize_results(results, count, row_index=row_index)
    return HttpResponse(json.dumps(serialized))


def direct_search(request):
    """
    Perform a direct target search. User selects TFs, species, and organ, and
    we return a ranked list of genes.
    """
    form = QueryDB_SearchForm(request.POST or None)
    if not form.is_valid():
        pass #I'm not sure what this response should contain.
    print form.cleaned_data
    #Get a list of genes that matches the query. Figure out their score, and
    #then drop the ones below the threshold somehow
    results = Experiment.objects.all()
    row_index = int(form.cleaned_data.pop('row_index'))
    species = None
    if form.cleaned_data['transcription_factor']:
        tfs = json.loads(form.cleaned_data.pop('transcription_factor'))
        results = results.filter(transcription_factor__in=tfs)
    if form.cleaned_data['species']:
        species = json.loads(form.cleaned_data.pop('species'))
        results = results.filter(species__in=species)
    if form.cleaned_data['organ']:
        species = json.loads(form.cleaned_data.pop('organ'))
        results = results.filter(expt_tissue__in=organ)
    genes = {}
    genes_to_show = set()
    for result in results:
        score = genes.get(result.gene) or 0
        score = score + EXPT_WEIGHTS[result.expt_type] * result.quality_factor
        genes[result.gene] = score
        if score > DIRECT_TARGET_THRESHOLD:
            genes_to_show.add(result.gene)

    final_results = Experiment.objects.get(gene__in=genes_to_show)
    actual_results = sorted(final_results, key=lambda r: genes[r.gene])
    serialized = _serialized(actual_results, final_results.count())
    return HttpResponse(json.dumps(serialized))


def download(request, size):
    form = QueryDB_SearchForm(request.POST or None)
    if not form.is_valid():
        return HttpResponse('Invalid form %s.' % form.errors)
    results, count, row_index = _search(form)
    if size == 'all':
        serialized_results = _serialize_results(results, count)['results']
    elif size == 'page':
        serialized_results = _serialize_results(results, count,
                                                row_index=row_index)['results']
    data = tablib.Dataset(headers=serialized_results[0].keys())
    data.json = json.dumps(serialized_results)
    filepath, fileid = _get_filepath()
    with open(os.path.join(settings.DOWNLOAD_DIR, filepath), 'wb') as fp:
        # Use tsv here to get tab-separated values
        fp.write(data.csv)
    return HttpResponse('{"url": "download_file/%d"}' % fileid)


def download_file(request, fileid):
    filepath, fileid = _get_filepath(fileid=fileid)
    with open(os.path.join(settings.DOWNLOAD_DIR, filepath), 'r') as fp:
        response = HttpResponse(fp.read(), content_type='application/csv')
        response['Content-Disposition'] = ('attachment; filename=%s' %
                                           os.path.basename(fp.name))
        return response


def _get_filepath(fileid=None):
    fileid = fileid or random.randint(0, 1000000)
    filepath = 'tftarget-search-%d.csv' % int(fileid)
    return filepath, fileid


def _serialize_results(results, count, row_index=None):
    """Takes the results set and serializes it"""
    if row_index is not None:
        results = results[row_index:row_index+100]
    results = [expt.serialize() for expt in results]
    return {'results': results, 'num_results': count}
