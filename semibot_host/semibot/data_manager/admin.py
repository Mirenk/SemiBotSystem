from django.contrib import admin

from .models import *

admin.site.register(Candidate)
admin.site.register(Label)
admin.site.register(LabelSet)
admin.site.register(LabelValue)
admin.site.register(Task)
admin.site.register(TaskRequest)

