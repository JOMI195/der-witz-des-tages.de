from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import SubmittedJoke, Joke
import Levenshtein


def is_similar_joke(submitted_text, existing_text, threshold=0.8):
    """
    Checks if the submitted joke is similar to an existing joke.
    Similarity is determined using Levenshtein distance.
    A threshold of 0.8 means 80% similarity.
    """
    distance = Levenshtein.ratio(submitted_text, existing_text)
    return distance >= threshold


@receiver(post_save, sender=SubmittedJoke)
def create_joke_from_submitted(sender, instance, created, **kwargs):
    if instance.is_approved:
        existing_jokes = Joke.objects.all()
        for joke in existing_jokes:
            if is_similar_joke(instance.text, joke.text):
                raise ValidationError(
                    f"Submitted joke is too similar to an existing joke (ID: {joke.id})."
                )

        with transaction.atomic():
            Joke.objects.create(
                text=instance.text,
                created_by=instance.created_by,
                joke_of_the_day_selection_weight=40,
            )
            instance.delete()
