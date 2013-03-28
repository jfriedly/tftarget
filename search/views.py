from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

from search.models import Experiment
from search.forms import SearchForm
from management.commands._constants import EXPT_TYPES, ALL_SPECIES, TRANSCRIPTION_FACTORS

import json


def search(request):
    """Search through the experiments for a search term."""
    form = SearchForm(request.POST or None)
    if not form.is_valid():
        tfs = [(a, b) for a, b in TRANSCRIPTION_FACTORS.iteritems()]
        species = [(a, a.capitalize()) for a in ALL_SPECIES]
        expts = [(a, b) for a, b in EXPT_TYPES.iteritems()]
        return render_to_response("search.html",
                                  {'form': form,
                                   'tf_choices': json.dumps(tfs),
                                   'tft_species':json.dumps(species),
                                   'tft_expt_types':json.dumps(expts)},
                                  context_instance=RequestContext(request))

    print form.cleaned_data
    
    results = Experiment.objects.all()
    page_num = int(form.cleaned_data.pop('page_number'))
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
 
    p = Paginator(results, 100) #100 is hard coded rows per page
    results = p.page(page_num ).object_list

    #this was the one taig a lot of time, but now t will only process 100 items
    for key, value in form.cleaned_data.iteritems():
        if value:
            results = results.filter(**{key: value})

   
    json_results = _serialize_results(results, p.count)
    return HttpResponse(json_results)


def _serialize_results(results, count):
    """Takes the results set and serializes it to JSON, adding transcription
    factors and experiment types.
    """
    results = list(results)
    for i, expt in enumerate(results):
        results[i] = expt.serialize()
    return json.dumps({'results': results,
                       'num_results': count})
