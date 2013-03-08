from django import forms

from search.models import Experiment


class SearchForm(forms.Form):
    """Search form to be submitted by a user."""
    transcription_factor = forms.CharField(label="Transcription Factor",
        widget=forms.HiddenInput(attrs={'class': 'tft-hidden input input-text'}),
        required=False)
    gene = forms.CharField(label="Gene",
        widget=forms.TextInput(attrs={'class': 'input input-text'}),
        required=False)
    species = forms.CharField(label="Species",
        widget=forms.HiddenInput(attrs={'class': 'input input-select'}),
        required=False)
    expt_type = forms.CharField(label="Experiment Name",
        widget=forms.HiddenInput(attrs={'class': 'input input-select'}),
        required=False)
    expt_tissues = forms.CharField(label="Organ",
        widget=forms.TextInput(attrs={'class': 'input input-text'}),
        required=False)
    page_number = forms.CharField(label="Page Number",
        widget=forms.HiddenInput(),
        required=False)
