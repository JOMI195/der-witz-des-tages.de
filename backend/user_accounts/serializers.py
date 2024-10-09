from rest_framework import serializers
from .models import Account


class AccountRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["recieves_newsletter"]


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["recieves_newsletter"]
