from django.urls import path
from .views import LessonUploadAPIView

urlpatterns = [
    path("upload/", LessonUploadAPIView.as_view(), name="lesson-upload"),
]
