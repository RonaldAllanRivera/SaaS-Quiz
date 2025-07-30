from rest_framework import serializers
from .models import Book, BookPage, BookQuiz, BookQuizQuestion, BookQuizAttempt, BookQuizAttemptAnswer

class BookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPage
        fields = ['order', 'text', 'image']

class BookSerializer(serializers.ModelSerializer):
    pages = BookPageSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'topic', 'grade_level', 'lexile', 'category', 'child', 'created_at', 'pages']

class BookQuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookQuizQuestion
        fields = ['id', 'question', 'type', 'options', 'answer', 'explanation', 'order']

class BookQuizSerializer(serializers.ModelSerializer):
    questions = BookQuizQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = BookQuiz
        fields = ['id', 'book', 'created_for_child', 'created_at', 'questions']

class BookQuizAttemptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookQuizAttemptAnswer
        fields = ['id', 'question', 'answer', 'is_correct']

class BookQuizAttemptSerializer(serializers.ModelSerializer):
    answers = BookQuizAttemptAnswerSerializer(many=True, read_only=True)
    class Meta:
        model = BookQuizAttempt
        fields = ['id', 'quiz', 'child', 'score', 'passed', 'created_at', 'completed_at', 'answers']
