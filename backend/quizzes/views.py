from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    QuizGenerateSerializer,
    QuizSerializer,
    QuestionSerializer,
    AnswerSubmitSerializer,
    AttemptSerializer,
    SpendTokensSerializer,  # Added
    ChildSerializer,  # Added
)
from .models import Quiz, Question, Child, Attempt, AttemptAnswer # Added
from lessons.models import LessonText
from typing import Any, Dict
import requests
import os
import json
import re
import uuid
from django.utils import timezone # Added


import uuid
from .models import Quiz, Question, Child  # Make sure Child is imported

class QuizGenerateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuizGenerateSerializer(data=request.data)
        if serializer.is_valid():
            validated_data: Dict[str, Any] = serializer.validated_data  # type: ignore
            lesson_id = validated_data['lesson_id']
            child_id = validated_data['child_id']  # Expect child_id in the payload

            try:
                lesson = LessonText.objects.get(id=lesson_id, parent=request.user)
            except LessonText.DoesNotExist:
                return Response({'error': 'Lesson not found.'}, status=404)

            try:
                child = Child.objects.get(id=child_id, parent=request.user)
            except Child.DoesNotExist:
                return Response({'error': 'Child not found.'}, status=404)

            openai_api_key = os.environ.get("OPENAI_API_KEY")
            openai_endpoint = "https://api.openai.com/v1/chat/completions"


            subject_name = (getattr(lesson.subject, "name", "") or "").lower().strip()

            if subject_name == "filipino":
                prompt = (
                    f"Ikaw ay isang guro ng elementarya. Gamit ang lesson text na ito:\n\n"
                    f"'''{lesson.content}'''\n\n"
                    f"Gumawa ng 10 tanong para sa asignaturang Filipino, na angkop sa batang nasa {child.get_grade_level_display()} (edad {child.age}). " # type: ignore[attr-defined]
                    "Gumamit ng simple, batang-wika na tanong. Para sa True or False questions, gamitin lamang ang mga pagpipilian na 'Tama' at 'Mali'. "
                    "Lahat ng tanong at sagot ay dapat nasa wikang Filipino. "
                    "Ibigay ang output bilang JSON list kung saan ang bawat tanong ay isang object: "
                    "{'type': 'mcq'|'tf', 'question': str, 'options': [str], 'answer': str}"
                )
            else:
                prompt = (
                    f"You are an elementary teacher. Using this lesson text:\n\n"
                    f"'''{lesson.content}'''\n\n"
                    f"Generate 10 quiz questions appropriate for a child in {child.get_grade_level_display()} (about age {child.age}). " # type: ignore[attr-defined]
                    "Use simple multiple choice and true/false only. Provide options for MCQ. "
                    "Format as a JSON list with each question as an object: "
                    "{'type': 'mcq'|'tf', 'question': str, 'options': [str], 'answer': str}"
                )

            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "gpt-4-1106-preview",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
            }
            openai_response = requests.post(openai_endpoint, json=payload, headers=headers)
            if openai_response.status_code == 200:
                result = openai_response.json()
                text = result["choices"][0]["message"]["content"]

                match = re.search(r"\[.*\]", text, re.DOTALL)
                if match is not None:
                    json_text = match.group()
                    try:
                        questions = json.loads(json_text)
                    except Exception:
                        return Response({"error": "Failed to parse quiz questions from OpenAI output.", "raw": text}, status=500)
                else:
                    return Response({"error": "Failed to parse quiz questions from OpenAI output.", "raw": text}, status=500)

                # === Unique link_slug logic ===
                unique_slug = str(uuid.uuid4())[:8]  # Short unique slug
                quiz = Quiz.objects.create(lesson=lesson, link_slug=unique_slug)

                for q in questions:
                    Question.objects.create(
                        quiz=quiz,
                        text=q.get('question'),
                        type=q.get('type'),
                        options=q.get('options', []),
                        answer=q.get('answer'),
                    )

                return Response({"quiz_id": getattr(quiz, "id", None), "questions": questions}, status=201)
            else:
                return Response({"error": "OpenAI API failed."}, status=500)
        return Response(serializer.errors, status=400)



class QuizListAPIView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # DRF Request always has .query_params, but Pylance may warn
        lesson_id = getattr(self.request, "query_params", None)
        lesson_id = lesson_id.get("lesson") if lesson_id else None
        qs = Quiz.objects.all()
        if lesson_id:
            qs = qs.filter(lesson__id=lesson_id)
        return qs.order_by("-created_at")


class QuizDetailAPIView(RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class QuizQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id, question_number):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            # Use related_name "questions" and silence static checker
            questions = getattr(quiz, "questions").order_by("id")
            question = questions[question_number - 1]  # question_number is 1-based
        except (Quiz.DoesNotExist, IndexError):
            return Response({"error": "Question not found."}, status=404)
        return Response(QuestionSerializer(question).data)



class QuizSubmitAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id, question_id):
        serializer = AnswerSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        child_id = request.data.get("child_id")
        if not child_id:
            return Response({"error": "Child ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = Question.objects.get(id=question_id, quiz_id=quiz_id)
            child = Child.objects.get(id=child_id, parent=request.user)
        except (Question.DoesNotExist, Child.DoesNotExist):
            return Response({"error": "Invalid quiz, question, or child."}, status=status.HTTP_404_NOT_FOUND)

        # Get or create an attempt for this quiz and child
        attempt, created = Attempt.objects.get_or_create(
            child=child, 
            quiz_id=quiz_id, 
            completed_at__isnull=True # Assumes one active attempt at a time
        )

        # Check if this question has already been answered in this attempt
        if AttemptAnswer.objects.filter(attempt=attempt, question=question).exists():
            return Response({"error": "This question has already been answered."}, status=status.HTTP_400_BAD_REQUEST)

        # Check answer and update score
        submitted_answer = serializer.validated_data["answer"]
        is_correct = (submitted_answer.strip().lower() == str(question.answer).strip().lower())

        if is_correct:
            attempt.score += 1

        # Record the answer
        AttemptAnswer.objects.create(
            attempt=attempt, 
            question=question, 
            answer=submitted_answer, 
            is_correct=is_correct
        )

        # Check if the quiz is complete
        total_questions = question.quiz.questions.count()
        answered_count = attempt.answers.count()

        if answered_count >= total_questions:
            attempt.completed_at = timezone.now()
            passing_score = total_questions * 0.7  # 70% to pass

            if attempt.score >= passing_score:
                attempt.passed = True
                child.tokens += 10  # Award 10 tokens for passing
                child.save()
        
        attempt.save()

        return Response(AttemptSerializer(attempt).data, status=status.HTTP_200_OK)


class SpendTokensAPIView(APIView):
    permission_classes = [IsAuthenticated]

    ITEM_COSTS = {
        "avatar": 50,
        "background": 100,
    }

    def post(self, request, *args, **kwargs):
        serializer = SpendTokensSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        child_id = request.data.get("child_id")
        if not child_id:
            return Response({"error": "Child ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            child = Child.objects.get(id=child_id, parent=request.user)
        except Child.DoesNotExist:
            return Response({"error": "Child not found."}, status=status.HTTP_404_NOT_FOUND)

        item_type = serializer.validated_data["item_type"]
        item_name = serializer.validated_data["item_name"]

        cost = self.ITEM_COSTS.get(item_type)
        if cost is None:
            return Response({"error": f"Invalid item type: {item_type}"}, status=status.HTTP_400_BAD_REQUEST)

        if child.tokens < cost:
            return Response({"error": "Not enough tokens."}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct tokens and update the child's profile
        child.tokens -= cost
        if item_type == "avatar":
            child.avatar = item_name
        elif item_type == "background":
            child.background = item_name
        
        child.save()

        return Response(ChildSerializer(child).data, status=status.HTTP_200_OK)

