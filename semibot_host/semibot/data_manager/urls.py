from django.urls import path, include
from rest_framework import routers

from .views import *

# REST APIのURL生成
routers = routers.DefaultRouter()
routers.register('candidates', CandidateViewSet)
routers.register('labels', LabelViewSet)
routers.register('labelsets', LabelSetViewSet)
routers.register('labelvalues', LabelValueViewSet)
routers.register('tasks', TaskViewSet)
routers.register('taskrequests', TaskRequestViewSet)

urlpatterns = [
    path('api/', include(routers.urls)),
]