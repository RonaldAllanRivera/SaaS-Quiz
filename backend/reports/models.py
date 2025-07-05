from django.db import models
from quizzes.models import Attempt

class Feedback(models.Model):
    attempt = models.OneToOneField(Attempt, on_delete=models.CASCADE, related_name="report_feedback")
    ai_review = models.TextField()
