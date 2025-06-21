from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_parent = models.BooleanField(default=True)  # Extend as needed
