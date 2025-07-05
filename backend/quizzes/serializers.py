from rest_framework import serializers
from .models import Quiz, Question, Child, Attempt, AttemptAnswer


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = "__all__"

class AttemptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttemptAnswer
        fields = ["id", "question", "answer", "is_correct"]


class AttemptSerializer(serializers.ModelSerializer):
    answers = AttemptAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Attempt
        fields = ["id", "child", "quiz", "score", "passed", "created_at", "completed_at", "answers"]

class SpendTokensSerializer(serializers.Serializer):
    item_type = serializers.ChoiceField(choices=["avatar", "background"])
    item_name = serializers.CharField(max_length=255)


class QuizGenerateSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    child_id = serializers.IntegerField()


class AnswerSubmitSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=100)


class FrontendQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ("answer",)



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class QuizSerializer(serializers.ModelSerializer):
    questions = FrontendQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "link_slug", "created_at", "lesson", "questions"]

