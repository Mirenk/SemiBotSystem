from django.contrib import admin

from .models import Candidate, Label

admin.site.register(Candidate)
admin.site.register(Label)

