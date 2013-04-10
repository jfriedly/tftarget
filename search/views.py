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
                               BINDING_EXPTS,
                               EXPRESSION_EXPTS,
                               DIRECT_SEARCH_THRESHOLD)


import settings


import os
import operator
import random
import json
import tablib

def index(request):
    qdb_form = QueryDB_SearchForm()
    dt_form = DirectTargets_SearchForm()
    return render_to_response("search.html",
                                  {'querydb_form': qdb_form,
                                   'direct_targets_form': dt_form,
                                   'tf_choices': json.dumps(TF_CHOICES),
                                   'tft_species':json.dumps(SPECIES_CHOICES),
                                   'tft_expt_types':json.dumps(EXPT_CHOICES)},
                                  context_instance=RequestContext(request))

def _search(form):
    results = Experiment.objects.all()
    row_index = int(form.cleaned_data.pop('row_index_2'))
    species = None
    if form.cleaned_data['transcription_factor_2']:
        tfs = json.loads(form.cleaned_data.pop('transcription_factor_2'))
        results = results.filter(transcription_factor__in=tfs)
    if form.cleaned_data['expt_type_2']:
        expts = json.loads(form.cleaned_data.pop('expt_type_2'))
        results = results.filter(expt_type__in=expts)
    if form.cleaned_data['species_2']:
        species = json.loads(form.cleaned_data.pop('species_2'))
        results = results.filter(species__in=species)
    if form.cleaned_data['gene_2']:
        gene = form.cleaned_data.pop('gene_2')
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
                                  {'querydb_form': form,
                                   'tf_choices': json.dumps(TF_CHOICES),
                                   'tft_species':json.dumps(SPECIES_CHOICES),
                                   'tft_expt_types':json.dumps(EXPT_CHOICES)},
                                  context_instance=RequestContext(request))

    results, count, row_index = _search(form)
    serialized = _serialize_results(results, count, 2, row_index=row_index)
    return HttpResponse(json.dumps(serialized))


def direct_search(request):
    """
    Perform a direct target search. User selects TFs, species, and organ, and
    we return a ranked list of genes.
    """
    form = DirectTargets_SearchForm(request.POST or None)
    print form
    if not form.is_valid():
        return render_to_response("search.html",
                                  {'direct_targets_form': form,
                                   'tf_choices': json.dumps(TF_CHOICES),
                                   'tft_species':json.dumps(SPECIES_CHOICES),
                                   'tft_expt_types':json.dumps(EXPT_CHOICES)},
                                  context_instance=RequestContext(request))
    print form.cleaned_data
    #Get a list of genes that matches the query. Figure out their score, and
    #then drop the ones below the threshold
    results = Experiment.objects.all()
    row_index = 0
    species = None
    if form.cleaned_data['transcription_factor_0']:
        tfs = json.loads(form.cleaned_data.pop('transcription_factor_0'))
        results = results.filter(transcription_factor__in=tfs)
    if form.cleaned_data['species_0']:
        species = json.loads(form.cleaned_data.pop('species_0'))
        results = results.filter(species__in=species)
    if form.cleaned_data['expt_tissues_0']:
        organ = json.loads(form.cleaned_data.pop('expt_tissues_0'))
        results = results.filter(expt_tissues__in=organ)
    # Map genes to their score (cumulatively)
    genes = {}
    # Add genes to this as we see their score get high enough
    genes_above_threshold = set()
    genes_with_binding = set()
    genes_with_expression = set()
    for result in results:
        score = genes.get(result.gene) or 0
        score = score + EXPT_WEIGHTS[result.expt_type] * result.quality_factor
        genes[result.gene] = score
        if score > DIRECT_SEARCH_THRESHOLD:
            genes_above_threshold.add(result.gene)
        if result.expt_type in BINDING_EXPTS:
            genes_with_binding.add(result.gene)
        elif result.expt_type in EXPRESSION_EXPTS:
            genes_with_expression.add(result.gene)

    # We want the ones with both experiment classes and above the threshold
    genes_to_show = (genes_above_threshold & genes_with_binding
                     & genes_with_expression)

    # Now we know what genes to show, so figure out which results involve them
    results_to_show = set()
    for r in results:
        if r.gene in genes_to_show:
            #FIXME This line is for testing only!! It should be removed prior
            #to delivery.
            r.transcription_factor = r.transcription_factor + ' '+str(genes[r.gene])

            results_to_show.add(r)
    # Now figure out what order to show them in
    actual_results = sorted(results_to_show, key=lambda r: genes[r.gene],
                            reverse=True)
    #And finally, show them
    serialized = _serialize_results(actual_results, len(actual_results), 0, None)
    return HttpResponse(json.dumps(serialized))


def download(request, size):
    form = QueryDB_SearchForm(request.POST or None)
    if not form.is_valid():
        return HttpResponse('Invalid form %s.' % form.errors)
    results, count, row_index = _search(form)
    if size == 'all':
        serialized_results = _serialize_results(results,
                                                count, csv=True)['results']
    elif size == 'page':
        serialized_results = _serialize_results(results, count,
                                                row_index=row_index,
                                                csv=True)['results']
    data = tablib.Dataset(headers=serialized_results[0].keys())
    data.json = json.dumps(serialized_results)
    filepath, fileid = _get_filepath()
    with open(os.path.join(settings.DOWNLOAD_DIR, filepath), 'wb') as fp:
        # Use tsv here to get tab-separated values
        fp.write(data.csv)
    return HttpResponse('{"url": "/download_file/%d"}' % fileid)


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

def _serialize_results(results, count, tab_num, row_index=None, csv=False):
    """Takes the results set and serializes it"""
    if row_index is not None:
        results = results[row_index:row_index+100]
    results = [expt.serialize(csv=csv) for expt in results]
    return {'results': results, 'num_results': count, 'tab_num':tab_num}
