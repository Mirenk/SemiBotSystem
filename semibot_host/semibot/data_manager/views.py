from rest_framework import viewsets
from .serializer import CandidateSerializer, LabelSerializer, LabelSetSerializer, LabelValueSerializer

from .models import Candidate, Label, LabelSet, LabelValue

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
