from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from search.models import Experiment
from search.forms import SearchForm

import settings

import os
import random
import json
import tablib


def _search(form):
    print form.cleaned_data
    results = Experiment.objects.all()
    row_index = int(form.cleaned_data.pop('row_index'))
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
        results = results.filter(gene__human=gene)

    for key, value in form.cleaned_data.iteritems():
        if value:
            results = results.filter(**{key: value})
    count = results.count()
    return results, count, row_index


def search(request):
    """Search through the experiments for a search term."""
    form = SearchForm(request.POST or None)
    if not form.is_valid():
        return render_to_response("search.html",
                                  {'form': form,
                                   'tf_choices': json.dumps(Experiment.TF_CHOICES),
                                   'tft_species':json.dumps(Experiment.SPECIES),
                                   'tft_expt_types':json.dumps(Experiment.EXPERIMENT_TYPES)},
                                  context_instance=RequestContext(request))

    results, count, row_index = _search(form)
    serialized = _serialize_results(results, count, row_index=row_index)
    return HttpResponse(json.dumps(serialized))


def download(request, size):
    form = SearchForm(request.POST or None)
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
        fp.write(data.tsv)
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
