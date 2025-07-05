import os
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeedbackSerializer, FeedbackGenerateSerializer
from .models import Feedback
from quizzes.models import Attempt, AttemptAnswer


class AIReportFeedbackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FeedbackGenerateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        attempt_id = serializer.validated_data['attempt_id']

        try:
            attempt = Attempt.objects.get(id=attempt_id, child__parent=request.user)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        if Feedback.objects.filter(attempt=attempt).exists():
            return Response({"error": "Feedback for this attempt has already been generated."}, status=status.HTTP_400_BAD_REQUEST)
        
        incorrect_answers = AttemptAnswer.objects.filter(attempt=attempt, is_correct=False)
        if not incorrect_answers.exists():
            return Response({"message": "No incorrect answers to review. Great job!"}, status=status.HTTP_200_OK)

        failed_questions_text = ""
        for ans in incorrect_answers:
            question = ans.question
            failed_questions_text += f"- Question: {question.text}\n  Your Answer: {ans.answer}\n  Correct Answer: {question.answer}\n\n"

        child = attempt.child
        prompt = (
            f"You are a friendly and encouraging tutor for a {child.age}-year-old child in {child.get_grade_level_display()}. "
            f"The child has just completed a quiz. Based on their incorrect answers, provide a short, positive, and simple review. "
            f"Focus on explaining the concepts behind the wrong answers in a way a child can understand. "
            f"Keep it under 100 words. Address the child by their name, {child.name}.\n\n"
            f"Here are the questions they got wrong:\n{failed_questions_text}"
            f"Please provide a helpful and encouraging review."
        )

        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key:
            return Response({"error": "OpenAI API key is not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
        }

        try:
            openai_response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            if openai_response.status_code >= 400:
                error_details = openai_response.json()
                print(f"OpenAI API Error: {error_details}")  # For server-side logging
                return Response(
                    {"error": "AI report generation failed.", "details": error_details},
                    status=openai_response.status_code,
                )

            result = openai_response.json()
            ai_review = result["choices"][0]["message"]["content"].strip()

        except requests.exceptions.RequestException as e:
            # This handles network errors
            return Response({"error": f"Failed to connect to OpenAI: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (KeyError, IndexError):
            # This handles unexpected response structure
            return Response({"error": "Failed to parse OpenAI response."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        feedback = Feedback.objects.create(attempt=attempt, ai_review=ai_review)

        return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)

