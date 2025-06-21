from django.db import models
from users.models import User

class Subject(models.Model):
    name = models.CharField(max_length=50)

class LessonText(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
