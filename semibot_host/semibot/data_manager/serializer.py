from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Candidate, Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']

class CandidateSerializer(serializers.ModelSerializer):
    label = LabelSerializer(many=True)

    class Meta:
        model = Candidate
        fields = ['id', 'username', 'first_name', 'last_name', 'label', 'message_addr']
