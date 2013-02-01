from django import forms

from search.models import Experiment, Experiment_Type


class SearchForm(forms.Form):
    """Search form to be submitted by a user."""
    transcription_family = forms.ChoiceField(label=("Transcription Factor "
        "Family"),
        choices=Experiment.TF_FAMILIES,
        widget=forms.Select(attrs={'class': 'input input-select'}),
        required=False)
    transcription_factor = forms.CharField(label="Transcription Factor",
        widget=forms.TextInput(attrs={'class': 'input input-text'}),
        required=False)
    gene = forms.CharField(label="Gene",
        widget=forms.TextInput(attrs={'class': 'input input-text'}),
        required=False)
    species = forms.ChoiceField(label="Species",
        choices=Experiment.SPECIES,
        widget=forms.Select(attrs={'class': 'input input-select'}),
        required=False)
    expt_name = forms.ChoiceField(label="Experiment Name",
        choices=Experiment_Type.EXPERIMENT_TYPES,
        widget=forms.Select(attrs={'class': 'input input-select'}),
        required=False)
    tissue_name = forms.CharField(label="Tissue Name",
        widget=forms.TextInput(attrs={'class': 'input input-text'}),
        required=False)
