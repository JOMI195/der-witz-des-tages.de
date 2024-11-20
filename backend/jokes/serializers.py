from rest_framework import serializers
from .models import Joke, JokeOfTheDay, JokePicture, SubmittedJoke


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
    created_by = serializers.SerializerMethodField()
    joke_picture = serializers.SerializerMethodField()
    shareable_image = serializers.SerializerMethodField()
    joke_of_the_day_created_at = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        username = (
            "jomi" if obj.created_by.username == "admin" else obj.created_by.username
        )
        creator = {
            "username": username,
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

    def get_shareable_image(self, obj):
        try:
            return {
                "image": obj.shareable_image.image.url,
                "created_at": obj.shareable_image.created_at,
            }
        except Joke.shareable_image.RelatedObjectDoesNotExist:
            return None

    def get_joke_of_the_day_created_at(self, obj):
        try:
            return obj.joke_of_the_day.first().created_at
        except AttributeError:
            return None

    class Meta:
        model = Joke
        fields = [
            "id",
            "text",
            "created_at",
            "created_by",
            "joke_picture",
            "shareable_image",
            "joke_of_the_day_created_at",
        ]


class JokeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = "__all__"
