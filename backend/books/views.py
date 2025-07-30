from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Book, BookPage, BookQuiz, BookQuizQuestion, BookQuizAttempt, BookQuizAttemptAnswer
from .serializers import BookSerializer, BookQuizSerializer, BookQuizAttemptSerializer
from quizzes.models import Child
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
import requests
import os
from .utils import download_and_save_image

class BookGenerateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Validate input
        topic = request.data.get('topic')
        grade_level = request.data.get('grade_level')
        lexile = request.data.get('lexile')
        child_id = request.data.get('child_id')
        if not all([topic, grade_level, lexile, child_id]):
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        child = get_object_or_404(Child, id=child_id, parent=request.user)

        # Call OpenAI for story text (stub)
        story_title = f"The {topic} Adventure"
        story_pages = [
            {'text': f"Once upon a time in {topic} land...", 'keyword': topic},
            {'text': f"The adventure continues for grade {grade_level} with lexile {lexile}.", 'keyword': topic}
        ]
        # Limit to 2-3 pages for speed

        # Fetch images from Pixabay (stub, one per page)
        pixabay_key = os.getenv('PIXABAY_API_KEY', getattr(settings, 'PIXABAY_API_KEY', None))
        print(f"[DEBUG] Using PIXABAY_API_KEY: {pixabay_key}")
        pages_with_images = []
        for idx, page in enumerate(story_pages):
            image_url = None
            try:
                api_url = f"https://pixabay.com/api/?key={pixabay_key}&q={page['keyword']}&image_type=photo&safesearch=true&per_page=3"
                print(f"[DEBUG] Pixabay API URL: {api_url}")
                resp = requests.get(api_url)
                print(f"[DEBUG] Pixabay Response: {resp.text}")
                data = resp.json()
                if data.get('hits'):
                    image_url = data['hits'][0]['webformatURL']
                print(f"[DEBUG] image_url for page {idx+1}: {image_url}")
            except Exception as e:
                print(f"[DEBUG] Pixabay fetch exception: {e}")
                image_url = None
            pages_with_images.append({'text': page['text'], 'image_url': image_url})

        # Save Book and Pages
        with transaction.atomic():
            book = Book.objects.create(
                title=story_title,
                topic=topic,
                grade_level=grade_level,
                lexile=lexile,
                category='Story',
                child=child
            )
            for order, page in enumerate(pages_with_images, 1):
                image_path = download_and_save_image(page['image_url'], topic, order)
                BookPage.objects.create(book=book, text=page['text'], image=image_path, order=order)
        book.refresh_from_db()
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

class BookQuizGenerateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        story_id = request.data.get('story_id')
        child_id = request.data.get('child_id')
        book = get_object_or_404(Book, id=story_id)
        child = get_object_or_404(Child, id=child_id, parent=request.user)
        # Call OpenAI for quiz questions (stub)
        questions = [
            {'question': 'What is the main topic?', 'type': 'multiple_choice', 'options': [book.topic, 'Other'], 'answer': book.topic, 'explanation': 'Topic from story', 'order': 1},
            {'question': 'Is this story fiction?', 'type': 'true_false', 'options': ['True', 'False'], 'answer': 'True', 'explanation': '', 'order': 2}
        ]
        with transaction.atomic():
            quiz = BookQuiz.objects.create(book=book, created_for_child=child)
            for q in questions:
                BookQuizQuestion.objects.create(quiz=quiz, **q)
        quiz.refresh_from_db()
        return Response(BookQuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
