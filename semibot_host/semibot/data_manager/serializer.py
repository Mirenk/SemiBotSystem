from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Candidate, Label, LabelSet, LabelValue, Task, TaskRequest

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']

class LabelSetSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()

    class Meta:
        model = LabelSet
        fields = ['id', 'name', 'labels']

    def get_labels(self, obj):
        try:
            label_abstract_contents = LabelSerializer(Label.objects.filter(label_set=LabelSet.objects.get(id=obj.id)), many=True).data
            return label_abstract_contents
        except:
            label_abstract_contents = None
            return label_abstract_contents

class CandidateSerializer(serializers.ModelSerializer):
    label = LabelSerializer(many=True)

    class Meta:
        model = Candidate
        fields = ['id', 'username', 'first_name', 'last_name', 'label', 'message_addr']

class LabelValueSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = LabelValue
        fields = ['id', 'label', 'value']

class TaskSerializer(serializers.ModelSerializer):
    require_label_value = LabelValueSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'require_label_value']

class TaskRequestSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    worker = CandidateSerializer(many=True)
    candidate = CandidateSerializer(many=True)
    recommend_label_value = LabelValueSerializer(many=True)

    class Meta:
        model = TaskRequest
        fields = ['id', 'task', 'work_datetime', 'worker', 'candidate', 'recommend_label_value', 'is_complete']