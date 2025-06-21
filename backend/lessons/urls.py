from django.urls import path
from .views import LessonUploadAPIView, SubjectListAPIView, ParentLessonListAPIView

urlpatterns = [
    path("upload/", LessonUploadAPIView.as_view(), name="lesson-upload"),
    path("subjects/", SubjectListAPIView.as_view(), name="subject-list"),
    path("my-lessons/", ParentLessonListAPIView.as_view(), name="parent-lesson-list"),
]