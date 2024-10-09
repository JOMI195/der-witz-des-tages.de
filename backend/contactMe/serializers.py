from rest_framework import serializers


class ContactMeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    subject = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=2000)
