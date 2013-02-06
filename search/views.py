from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from search.models import Experiment
from search.forms import SearchForm


def search(request):
    """Search through the experiments for a search term."""
    form = SearchForm(request.POST or None)
    if not form.is_valid():
        return render_to_response("search.html", {"form": form},
                                  context_instance=RequestContext(request))
    results = set()
    if form.cleaned_data['expt_type']:
        expt_type = form.cleaned_data.pop('expt_type')
        experiments = Experiment.objects.filter(expt_type__type_name=expt_type)
        results = _intersect_unless_empty(results, experiments)

    if form.cleaned_data['tissue_name']:
        tissue = form.cleaned_data.pop('tissue_name')
        experiments = Experiment.objects.filter(experimental_tissues=tissue)
        results = _intersect_unless_empty(results, experiments)

    for key, value in form.cleaned_data.iteritems():
        if value:
            these_results = Experiment.objects.filter(**{key: value})
            results = _intersect_unless_empty(results, these_results)
    return HttpResponse(str(list(results)))


def _intersect_unless_empty(results, these_results):
    """Takes the final results set and a set of results matching one parameter
    and returns the intersection of them if the final results set is non-empty,
    else returns the set matching that parameter.
    """
    if results and these_results:
        return results.intersection(set(these_results))
    return set(these_results)
