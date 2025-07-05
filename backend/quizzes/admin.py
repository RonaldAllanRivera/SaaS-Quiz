from django.contrib import admin
from .models import Quiz, Question, Child, Attempt, AttemptAnswer, Feedback

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Child)
admin.site.register(Attempt)
admin.site.register(AttemptAnswer)
admin.site.register(Feedback)
