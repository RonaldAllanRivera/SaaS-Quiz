from rest_framework import serializers
from .models import Quiz, Question, Child, Attempt


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = "__all__"

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = "__all__"

class QuizGenerateSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "link_slug", "created_at", "lesson", "questions"]
