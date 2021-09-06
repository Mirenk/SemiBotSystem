from rest_framework import viewsets
from .serializer import *
from django_filters import rest_framework as filters

from .models import *

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

class LabelSetViewSet(viewsets.ModelViewSet):
    queryset = LabelSet.objects.all()
    serializer_class = LabelSetSerializer

class LabelValueViewSet(viewsets.ModelViewSet):
    queryset = LabelValue.objects.all()
    serializer_class = LabelValueSerializer
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

##
## 依頼REST API
##
# フィルタ
class TaskRequestFilter(filters.FilterSet):
    is_complete = filters.BooleanFilter()
    work_datetime_lt = filters.DateTimeFilter(field_name='work_datetime', lookup_expr='lt')

    class Meta:
        model = TaskRequest
        fields = ['is_complete', 'work_datetime_lt']

# ViewSet
class TaskRequestViewSet(viewsets.ModelViewSet):
    queryset = TaskRequest.objects.all()
    serializer_class = TaskRequestSerializer
    filter_class = TaskRequestFilter
