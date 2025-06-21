from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import LessonUploadSerializer, SubjectSerializer, LessonTextSerializer
from .models import LessonText, Subject
import requests
import base64
import os
from typing import Any, Dict  # Added for static type hinting

class LessonUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LessonUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Explicitly tell Pylance: validated_data is a dict
            validated_data: Dict[str, Any] = serializer.validated_data  # type: ignore
            image = validated_data['image']
            subject = validated_data['subject']

            # Optional: extra runtime check if you want defensive code
            if not image or not subject:
                return Response({"error": "Image and subject are required."}, status=400)

            # Convert image to base64
            image_b64 = base64.b64encode(image.read()).decode("utf-8")

            openai_api_key = os.environ.get("OPENAI_API_KEY")
            openai_endpoint = "https://api.openai.com/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json",
            }

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Extract and summarize only the elementary-relevant lesson content from this image. "
                        f"Ignore names and extra text not related to the subject: {getattr(subject, 'name', str(subject))}."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": f"data:image/png;base64,{image_b64}"
                        }
                    ],
                },
            ]

            payload = {
                "model": "gpt-4-vision-preview",
                "messages": messages,
                "max_tokens": 1024,
            }

            openai_response = requests.post(openai_endpoint, json=payload, headers=headers)
            if openai_response.status_code == 200:
                result = openai_response.json()
                extracted_text = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

                # Save to DB
                lesson = LessonText.objects.create(
                    parent=request.user,
                    subject=subject,
                    content=extracted_text,
                )
                # No warning for .id, but can still use getattr for silence
                return Response({"id": getattr(lesson, "id", None), "content": extracted_text}, status=201)
            else:
                return Response({"error": "OpenAI Vision API failed."}, status=500)
        return Response(serializer.errors, status=400)


class SubjectListAPIView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ParentLessonListAPIView(ListAPIView):
    serializer_class = LessonTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # request.user is always available here
        return LessonText.objects.filter(parent=self.request.user).order_by('-created_at')
