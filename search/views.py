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
        return render_to_response("search.html", {"form": form},
                                  context_instance=RequestContext(request))
    results = set()
    if form.cleaned_data['transcription_factor']:
        try:
            tf = json.loads('"%s"' % form.cleaned_data['transcription_factor'])
            experiments = Experiment.objects.filter(transcription_factor=tf)
            form.cleaned_data.pop('transcription_factor')
        except ValueError:
            tfs = json.loads(form.cleaned_data.pop('transcription_factor'))
            experiments = set()
            for tf in tfs:
                experiments = experiments.union(set(Experiment.objects.filter(transcription_factor=tf)))
        results = _intersect_unless_empty(results, experiments)

    for key, value in form.cleaned_data.iteritems():
        if value:
            these_results = Experiment.objects.filter(**{key: value})
            results = _intersect_unless_empty(results, these_results)
    json_results = _serialize_results(results)
    return HttpResponse(json_results)


def _intersect_unless_empty(results, these_results):
    """Takes the final results set and a set of results matching one parameter
    and returns the intersection of them if the final results set is non-empty,
    else returns the set matching that parameter.
    """
    if results and these_results:
        return results.intersection(set(these_results))
    return set(these_results)


def _serialize_results(results):
    """Takes the results set and serializes it to JSON, adding transcription
    factors and experiment types.
    """
    full_results = []
    for expt in list(results):
        expt = expt.serialize()
        full_results.append(expt)
    print str(results)
    print json.dumps(full_results)
    return json.dumps(full_results)
