from django.urls import path
from .views import AIReportFeedbackAPIView

urlpatterns = [
    path("generate/", AIReportFeedbackAPIView.as_view(), name="report-generate"),
]
