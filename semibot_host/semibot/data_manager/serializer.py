from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Candidate, Label, LabelSet

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']

class LaberSetSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()

    class Meta:
        model = LabelSet
        fields = ['id', 'name', 'labels']

    def get_labels(self, obj):
        try:
            label_abstruct_contents = LabelSerializer(Label.objects.filter(labelset=LabelSet.objects.get(id=obj.id)), many=True).data
            return label_abstruct_contents
        except:
            label_abstruct_contents = None
            return label_abstruct_contents

class CandidateSerializer(serializers.ModelSerializer):
    label = LabelSerializer(many=True)

    class Meta:
        model = Candidate
        fields = ['id', 'username', 'first_name', 'last_name', 'label', 'message_addr']
