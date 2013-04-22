from django import forms


class QueryDBSearchForm(forms.Form):
    """Search form to be submitted by a user."""
    attrs = {'class': 'query_db'}
    gene_attrs = {'class': 'input-text span3 query_db'}
    hidden_attrs = {'class': 'tft-hidden query_db'}
    transcription_factor = forms.CharField(label="Transcription Factor",
        widget=forms.HiddenInput(attrs=hidden_attrs), required=False)
    gene = forms.CharField(label="Gene",
        widget=forms.TextInput(attrs=gene_attrs), required=False)
    species = forms.CharField(label="Species",
        widget=forms.HiddenInput(attrs=hidden_attrs), required=False)
    expt_type = forms.CharField(label="Experiment Name",
        widget=forms.HiddenInput(attrs=hidden_attrs), required=False)
    expt_tissues = forms.CharField(label="Organ",
        widget=forms.HiddenInput(attrs=hidden_attrs), required=False)
    row_index = forms.CharField(label="Row Index",
        widget=forms.HiddenInput(attrs=attrs), required=False)


class DirectTargetsSearchForm(forms.Form):
    """Search form to be submitted by a user."""
    attrs = {'class': 'direct_targets'}
    hidden_attrs = {'class': 'tft-hidden direct_targets'}
    transcription_factor = forms.CharField(label="Transcription Factor",
        widget=forms.HiddenInput(attrs=hidden_attrs), required=False)
    species = forms.CharField(label="Species",
        widget=forms.HiddenInput(attrs=hidden_attrs), required=False)
    expt_tissues = forms.CharField(label="Organ",
        widget=forms.HiddenInput(attrs=hidden_attrs), required=False)
    row_index = forms.CharField(label="Row Index",
        widget=forms.HiddenInput(attrs=attrs), required=False)


class EnrichmentAnalysisSearchForm(forms.Form):
    """Search form to be submitted by a user."""
    attrs = {'class': 'enrichment_analysis'}
    gene_list = forms.CharField(label="Gene List",
        widget=forms.Textarea(attrs=attrs), required=True)
    species = forms.CharField(label="Species",
        widget=forms.HiddenInput(attrs=attrs), required=False)
    expt_tissues = forms.CharField(label="Organ",
        widget=forms.HiddenInput(attrs=attrs), required=False)
