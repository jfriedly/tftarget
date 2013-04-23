from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from search.models import Experiment, Gene
from search.forms import QueryDBSearchForm, EnrichmentAnalysisSearchForm, DirectTargetsSearchForm
from search._constants import (SPECIES_CHOICES,
                               TISSUE_CHOICES,
                               TF_CHOICES,
                               TFS,
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
import time
import copy
from scipy import stats


GLOBAL_TEMPLATE_PARAMS = {'tf_choices': json.dumps(TF_CHOICES),
                          'tft_species': json.dumps(SPECIES_CHOICES),
                          'tft_expt_types': json.dumps(EXPT_CHOICES),
                          'tft_tissue_choices': json.dumps(TISSUE_CHOICES)}


def index(request):
    """Returns the main page, filling in forms and a few object for the JS to
    parse.
    """
    dt_form = DirectTargetsSearchForm()
    ea_form = EnrichmentAnalysisSearchForm()
    qdb_form = QueryDBSearchForm()
    template_params = {'querydb_form': qdb_form,
                       'ea_form': ea_form,
                       'direct_targets_form': dt_form}
    template_params.update(GLOBAL_TEMPLATE_PARAMS)
    return render_to_response("search.html", template_params,
                              context_instance=RequestContext(request))


def _search_genes(gene_names, species=None):
    """Given a list of gene names and optionally a list of species, this
    function searches through all the Gene objects and returns the ones that
    match.
    """
    if species is not None:
        fnames = [s.lower() for s in species]
    else:
        fnames = [field.name for field in Gene._meta.fields]
        fnames.remove('id')
    if fnames:
        queries = (Q(**{name: gene}) for name in fnames for gene in gene_names)
        qgroup = reduce(operator.or_, queries)
        return Gene.objects.filter(qgroup)
    return []


def _search(form):
    """General search function.  Takes a valid ``DirectTargetsSearchForm`` or
    a valid ``QueryDBSearchForm`` and returns the raw DB search results,
    count, and row_index.
    """
    results = Experiment.objects.filter(active=True)
    print form.cleaned_data
    row_index = int(form.cleaned_data.pop('row_index', 0))
    if not any(form.cleaned_data.itervalues()):
        # If they didn't search for anything, don't return the entire DB
        return [], 0, row_index
    species = None
    if form.cleaned_data.get('transcription_factor', False):
        tfs = json.loads(form.cleaned_data.pop('transcription_factor'))
        results = results.filter(transcription_factor__in=tfs)
    if form.cleaned_data.get('expt_type', False):
        expts = json.loads(form.cleaned_data.pop('expt_type'))
        results = results.filter(expt_type__in=expts)
    if form.cleaned_data.get('species', False):
        species = json.loads(form.cleaned_data.pop('species'))
        results = results.filter(species__in=species)
    if form.cleaned_data.get('expt_tissues', False):
        tissues = json.loads(form.cleaned_data.pop('expt_tissues'))
        results = results.filter(expt_tissues__in=tissues)
    if form.cleaned_data.get('gene', False):
        gene = form.cleaned_data.pop('gene')
        genes = _search_genes([gene], species=species)
        if genes:
            results = results.filter(gene__in=genes)

    count = results.count()
    return results, count, row_index


def query_db(request):
    """Queries the database based on use input to the Query DB form and
    returns the raw results.
    """
    form = QueryDBSearchForm(request.POST or None)
    if not form.is_valid():
        template_params = {'querydb_form': form}
        template_params.update(GLOBAL_TEMPLATE_PARAMS)
        return render_to_response("search.html", template_params,
                                  context_instance=RequestContext(request))
    results, count, row_index = _search(form)
    serialized = _serialize_results(results, count, row_index=row_index)
    return HttpResponse(json.dumps(serialized))


def _direct_search(results, sort=False):
    """
    With an iterable of Experiments, remove the ones on genes which do not have
    both types of experiments and which are scored below the threshold. If
    ``sort`` is passed as True, return the results as a list sorted by the
    score. Otherwise, return the results in a Python list.
    """
    results = results.select_related('gene')
    # Map genes to their score (cumulatively)
    genes = {}
    # Add genes to this as we see their score get high enough
    genes_above_threshold = set()
    genes_with_binding = set()
    genes_with_expression = set()
    for result in results:
        score = genes.get(result.gene, 0)
        score += EXPT_WEIGHTS[result.expt_type] * result.quality_factor
        genes[result.gene] = score
        if score > DIRECT_SEARCH_THRESHOLD:
            genes_above_threshold.add(result.gene)
        if result.expt_type in BINDING_EXPTS:
            genes_with_binding.add(result.gene)
        else:
            genes_with_expression.add(result.gene)

    # We want the ones with both experiment classes and above the threshold
    genes_to_show = (genes_above_threshold & genes_with_binding
                     & genes_with_expression)

    # Now we know what genes to show, so figure out which results involve them
    results_to_show = set()
    for r in results:
        if r.gene in genes_to_show:
            results_to_show.add(r)
    # Now figure out what order to show them in, and return them
    if sort is True:
        return sorted(results_to_show, key=lambda r: genes[r.gene],
                      reverse=True)
    else:
        return list(results_to_show)


def direct_search(request):
    """
    Perform a direct target search. User selects TFs, species, and organ, and
    we return a ranked list of genes.
    """
    form = DirectTargetsSearchForm(request.POST or None)
    if not form.is_valid():
        template_params = {'direct_targets_form': form}
        template_params.update(GLOBAL_TEMPLATE_PARAMS)
        return render_to_response("search.html", template_params,
                                  context_instance=RequestContext(request))
    results, count, row_index = _search(form)
    sorted_results = _direct_search(results, sort=True)
    serialized = _serialize_results(sorted_results, len(sorted_results),
                                    tab_num=0, row_index=row_index)
    return HttpResponse(json.dumps(serialized))


@csrf_exempt
def download(request, size):
    """Prepares a DB query for download by creating a CSV and responding with
    a link to download the CSV from.
    """
    form = QueryDBSearchForm(request.POST or None)
    if not form.is_valid():
        template_params = {'querydb_form': form}
        template_params.update(GLOBAL_TEMPLATE_PARAMS)
        return render_to_response("search.html", template_params,
                                  context_instance=RequestContext(request))
    results, count, row_index = _search(form)
    if size == 'all':
        serialized_results = _serialize_results(results, count,
                                                csv=True)['results']
    elif size == 'page':
        serialized_results = _serialize_results(results, count,
                                                row_index=row_index,
                                                csv=True)['results']
    data = tablib.Dataset(headers=serialized_results[0].keys())
    data.json = json.dumps(serialized_results)
    filepath, fileid = _get_filepath()
    with open(os.path.join(settings.DOWNLOAD_DIR, filepath), 'wb') as fp:
        fp.write(data.csv)
    return HttpResponse('{"url": "/download_file/%d"}' % fileid)


def download_file(request, fileid):
    """Serves the CSV file with the fileid specified.
    """
    filepath, fileid = _get_filepath(fileid=fileid)
    with open(os.path.join(settings.DOWNLOAD_DIR, filepath), 'r') as fp:
        response = HttpResponse(fp.read(), content_type='application/csv')
        response['Content-Disposition'] = ('attachment; filename=%s' %
                                           os.path.basename(fp.name))
        return response


def _get_filepath(fileid=None):
    """Convenience function for turning a fileid into a filename if given,
    or creating one if not.
    """
    fileid = fileid or random.randint(0, 1000000)
    filepath = 'tftarget-search-%d.csv' % int(fileid)
    return filepath, fileid


def _serialize_results(results, count, tab_num=2, row_index=None, csv=False):
    """Takes the results set and serializes it

    tab_num refers to the index of the tab that these results are intended for.
    The tabs are Direct Targets, Enrichment Analysis, and Query DB.
    """
    if row_index is not None:
        results = results[row_index:row_index + 100]
    results = [expt.serialize(csv=csv) for expt in results]
    return {'results': results, 'num_results': count, 'tab_num': tab_num}


def enrichment_analysis(request):
    start = time.time()
    form = EnrichmentAnalysisSearchForm(request.POST or None)
    template_params = {'ea_form': form}
    template_params.update(GLOBAL_TEMPLATE_PARAMS)
    if not form.is_valid():
        return render_to_response("search.html", template_params,
                                  context_instance=RequestContext(request))
    print form.cleaned_data
    raw_user_list = form.cleaned_data['gene_list']
    user_list = set(s.strip(',') for s in raw_user_list.split())
    if len(user_list) == 0:
        return render_to_response("search.html", template_params,
                                  context_instance=RequestContext(request))
    user_list = set(_search_genes(user_list))
    print "User list is %s" % user_list
    all_genes = Gene.objects.all()
    results = []
    expts, count, row_index = _search(form)
    for tf in set(TFS.itervalues()):
        expts_for_loop = copy.deepcopy(expts)
        expts_for_loop = expts_for_loop.filter(transcription_factor=tf)
        targeted = set(expt.gene for expt in _direct_search(expts_for_loop))
        if len(targeted) == 0:
            print "Setting enrichment to 1.0 for %s" % tf
            enrichment = 1.0
        else:
            overlap = user_list.intersection(targeted)
            enrichment = stats.hypergeom.sf(len(overlap) - 1,
                                            all_genes.count(),
                                            len(user_list),
                                            len(targeted))
        results.append({'tf': tf, 'enrichment': enrichment})
    results = sorted(results, key=lambda tf: tf['tf'])
    print time.time() - start
    return HttpResponse(json.dumps(results))
