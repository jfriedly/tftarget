from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from search.models import Experiment, Transcription, Tissue
from search.forms import SearchForm


def search(request):
    """Search through the experiments for a search term."""
    form = SearchForm(request.POST or None)
    if not form.is_valid():
        return render_to_response("search.html", {"form": form},
                                  context_instance=RequestContext(request))
    results = set()
    if form.cleaned_data['tissue_name']:
        tissue_name = form.cleaned_data.pop('tissue_name')
        tissues = Tissue.objects.filter(tissue_name=tissue_name)
        results = _intersect_unless_empty(results,
                                          (t.expt_id for t in tissues))

    if form.cleaned_data['transcription_factor']:
        factor = form.cleaned_data.pop('transcription_factor')
        factors = Transcription.objects.filter(transcription_factor=factor)
        results = _intersect_unless_empty(results,
                                          (t.expt_id for t in factors))

    if form.cleaned_data['expt_name']:
        expt_name = form.cleaned_data.pop('expt_name')
        experiments = Experiment.objects.filter(expt_name__type_name=expt_name)
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
