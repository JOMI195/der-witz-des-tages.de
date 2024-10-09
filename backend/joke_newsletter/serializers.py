from rest_framework import serializers
from .models import NewsletterReciever


class NewsletterRecieverSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterReciever
        fields = "__all__"
