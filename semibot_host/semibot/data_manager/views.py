from rest_framework import viewsets
from .serializer import CandidateSerializer, LabelSerializer

from .models import Candidate, Label

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
