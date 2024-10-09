from rest_framework import serializers
from .models import Joke, JokePicture, SubmittedJoke


class JokePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = JokePicture
        fields = "__all__"


class SubmittedJokeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedJoke
        fields = ["id", "text", "created_at", "created_by", "is_approved"]
        read_only_fields = ["id", "created_at", "is_approved", "created_by"]

    def create(self, validated_data):
        created_by = self.context.get("created_by")
        if created_by:
            validated_data["created_by"] = created_by

        submitted_joke = SubmittedJoke.objects.create(**validated_data)
        return submitted_joke


class SubmittedJokeRetrieveSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        creator = {
            "username": obj.created_by.username,
        }
        return creator

    class Meta:
        model = SubmittedJoke
        fields = ["id", "text", "created_at", "created_by", "is_approved"]


class JokeRetrieveSerializer(serializers.ModelSerializer):
    joke_picture = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        creator = {
            "username": obj.created_by.username,
        }
        return creator

    def get_joke_picture(self, obj):
        try:
            return {
                "image": obj.joke_picture.image.url,
                "created_at": obj.joke_picture.created_at,
            }
        except Joke.joke_picture.RelatedObjectDoesNotExist:
            return None

    class Meta:
        model = Joke
        fields = [
            "id",
            "text",
            "created_at",
            "created_by",
            "joke_of_the_day_selection_weight",
            "joke_picture",
        ]


class JokeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = "__all__"
