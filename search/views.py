from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

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
