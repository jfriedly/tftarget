from django.contrib import admin
from search.models import Experiment, ExperimentType, TranscriptionFactor

admin.site.register(Experiment)
admin.site.register(ExperimentType)
admin.site.register(TranscriptionFactor)
