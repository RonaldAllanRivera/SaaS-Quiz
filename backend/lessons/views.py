from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import LessonUploadSerializer, SubjectSerializer, LessonTextSerializer
from rest_framework.permissions import IsAuthenticated
from .models import LessonText, Subject
from users.models import User
import requests
import base64
import os



class LessonUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = LessonUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            subject = serializer.validated_data['subject']

            # Convert image to base64
            image_b64 = base64.b64encode(image.read()).decode("utf-8")

            # Call OpenAI Vision API (example below)
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
                        f"Ignore names and extra text not related to the subject: {subject.name}."
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
                # Parse OpenAI result
                extracted_text = result["choices"][0]["message"]["content"].strip()
                
                # Save to DB
                lesson = LessonText.objects.create(
                    parent=request.user,
                    subject=subject,
                    content=extracted_text,
                )
                return Response({"id": lesson.id, "content": extracted_text}, status=201)
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
        return LessonText.objects.filter(parent=self.request.user).order_by('-created_at')
