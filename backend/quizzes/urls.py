from django.urls import path
from .views import (
    QuizGenerateAPIView,
    QuizListAPIView,
    QuizDetailAPIView,
    QuizQuestionAPIView,
    QuizSubmitAnswerAPIView,
    SpendTokensAPIView,  # Added

)

urlpatterns = [
    path("generate/", QuizGenerateAPIView.as_view(), name="quiz-generate"),
    path("", QuizListAPIView.as_view(), name="quiz-list"),
    path("<int:id>/", QuizDetailAPIView.as_view(), name="quiz-detail"),
    path("<int:quiz_id>/questions/<int:question_number>/", QuizQuestionAPIView.as_view(), name="quiz-question"),
    path("<int:quiz_id>/questions/<int:question_id>/submit/", QuizSubmitAnswerAPIView.as_view(), name="quiz-submit-answer"),
    path("rewards/spend/", SpendTokensAPIView.as_view(), name="spend-tokens"),
]