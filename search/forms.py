from django import forms

from search.models import Experiment


class QueryDB_SearchForm(forms.Form):
    """Search form to be submitted by a user."""
    transcription_factor_2 = forms.CharField(label="Transcription Factor",
        widget=forms.HiddenInput(attrs={'class': 'tft-hidden input input-text'}),
        required=False)
    gene_2 = forms.CharField(label="Gene",
        widget=forms.TextInput(attrs={'class': 'input input-text span3'}),
        required=False)
    species_2 = forms.CharField(label="Species",
        widget=forms.HiddenInput(attrs={'class': 'input input-select'}),
        required=False)
    expt_type_2 = forms.CharField(label="Experiment Name",
        widget=forms.HiddenInput(attrs={'class': 'input input-select'}),
        required=False)
    expt_tissues_2 = forms.CharField(label="Organ",
        widget=forms.HiddenInput(attrs={'class': 'input input-text'}),
        required=False)
    row_index_2 = forms.CharField(label="Row Index",
        widget=forms.HiddenInput(),
        required=False)


class DirectTargets_SearchForm(forms.Form):
    """Search form to be submitted by a user."""
    transcription_factor_0 = forms.CharField(label="Transcription Factor",
        widget=forms.HiddenInput(attrs={'class': 'tft-hidden input input-text'}),
        required=False)
    species_0 = forms.CharField(label="Species",
        widget=forms.HiddenInput(attrs={'class': 'input input-select'}),
        required=False)
    expt_tissues_0 = forms.CharField(label="Organ",
        widget=forms.HiddenInput(attrs={'class': 'input input-text'}),
        required=False)
    row_index_0 = forms.CharField(label="Row Index",
        widget=forms.HiddenInput(),
        required=False)


class GeneEnrichement_SearchForm(forms.Form):
    """Search form to be submitted by a user."""
    transcription_factor = forms.CharField(label="Transcription Factor",
        widget=forms.HiddenInput(attrs={'class': 'tft-hidden input input-text'}),
        required=False)
    gene_list = forms.CharField(label="Gene List",
        widget=forms.Textarea(attrs={'class': 'input input-text'}),
        required=False)
