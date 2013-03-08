from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from search.models import Experiment
from search.forms import SearchForm

import json


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
    json_results = _serialize_results(results, row_index, count)
    return HttpResponse(json_results)


def _serialize_results(results, row_index, count):
    """Takes the results set and serializes it to JSON, adding transcription
    factors and experiment types.
    """
    results = list(results)
    for i, expt in enumerate(results):
        results[i] = expt.serialize()
    return json.dumps({'results': results[row_index:row_index+100],
                       'num_results': count})
