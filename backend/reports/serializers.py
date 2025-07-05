from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackGenerateSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
