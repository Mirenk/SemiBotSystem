from rest_framework import viewsets
from .serializer import *

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
    
class TaskRequestViewSet(viewsets.ModelViewSet):
    queryset = TaskRequest.objects.all()
    serializer_class = TaskRequestSerializer
