from rest_framework import serializers
from .models import Subject, LessonText

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class LessonTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonText
        fields = "__all__"
