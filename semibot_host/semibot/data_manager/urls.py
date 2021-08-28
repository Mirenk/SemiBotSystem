from django.urls import path, include
from rest_framework import routers

from .views import CandidateViewSet, LabelViewSet

# REST APIのURL生成
routers = routers.DefaultRouter()
routers.register('candidates', CandidateViewSet)
routers.register('labels', LabelViewSet)

urlpatterns = [
    path('api/', include(routers.urls)),
]