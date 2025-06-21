from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from .serializers import QuizGenerateSerializer, QuizSerializer
from .models import Quiz, Question
from lessons.models import LessonText
import requests
import os



class QuizGenerateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuizGenerateSerializer(data=request.data)
        if serializer.is_valid():
            lesson_id = serializer.validated_data['lesson_id']

            # Get lesson and subject
            try:
                lesson = LessonText.objects.get(id=lesson_id, parent=request.user)
            except LessonText.DoesNotExist:
                return Response({'error': 'Lesson not found.'}, status=404)

            # Use OpenAI to generate questions
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            openai_endpoint = "https://api.openai.com/v1/chat/completions"

            prompt = (
                f"You are an elementary teacher. Using this lesson text:\n\n"
                f"'''{lesson.content}'''\n\n"
                f"Generate 10 simple quiz questions for elementary students. "
                "Use multiple choice and true/false only. Provide options for MCQ. "
                "Format as a JSON list with each question as an object: "
                "{'type': 'mcq'|'tf', 'question': str, 'options': [str], 'answer': str}"
            )

            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "gpt-4-1106-preview",  # or your preferred model
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1024,
            }
            openai_response = requests.post(openai_endpoint, json=payload, headers=headers)
            if openai_response.status_code == 200:
                result = openai_response.json()
                text = result["choices"][0]["message"]["content"]

                # Try to parse the JSON list from the LLM output
                import json
                import re

                try:
                    json_text = re.search(r"\[.*\]", text, re.DOTALL).group()
                    questions = json.loads(json_text)
                except Exception:
                    return Response({"error": "Failed to parse quiz questions from OpenAI output.", "raw": text}, status=500)

                # Save Quiz and Questions to DB
                from lessons.models import Subject
                quiz = Quiz.objects.create(lesson=lesson)
                for q in questions:
                    Question.objects.create(
                        quiz=quiz,
                        text=q.get('question'),
                        type=q.get('type'),
                        options=q.get('options', []),
                        answer=q.get('answer'),
                    )

                return Response({"quiz_id": quiz.id, "questions": questions}, status=201)
            else:
                return Response({"error": "OpenAI API failed."}, status=500)
        return Response(serializer.errors, status=400)


class QuizListAPIView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.request.query_params.get("lesson")
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
            # Order questions by id or a specific order if you wish
            questions = quiz.question_set.order_by("id")
            question = questions[question_number - 1]  # question_number is 1-based
        except (Quiz.DoesNotExist, IndexError):
            return Response({"error": "Question not found."}, status=404)
        from .serializers import QuestionSerializer
        return Response(QuestionSerializer(question).data)
