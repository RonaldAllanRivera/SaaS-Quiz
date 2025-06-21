from django.db import models
from quizzes.models import Attempt

class Feedback(models.Model):
    attempt = models.OneToOneField(Attempt, on_delete=models.CASCADE)
    ai_review = models.TextField()
