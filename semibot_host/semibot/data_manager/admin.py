from django.contrib import admin

from .models import Candidate, Label, LabelSet

admin.site.register(Candidate)
admin.site.register(Label)
admin.site.register(LabelSet)

