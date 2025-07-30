from django.urls import path
from .views import BookGenerateAPIView, BookQuizGenerateAPIView

urlpatterns = [
    path('generate/', BookGenerateAPIView.as_view(), name='book-generate'),
    path('quiz/', BookQuizGenerateAPIView.as_view(), name='book-quiz-generate'),
]
