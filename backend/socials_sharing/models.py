from django.db import models

from jokes.models import Joke


class InstagramShare(models.Model):
    """
    Ledger of what actually reached Instagram.

    The unique constraint is what makes the backfill safe to retry: a joke can
    never be posted to the feed twice, no matter how often a task is redelivered.
    """

    FEED = "feed"
    STORY = "story"
    KIND_CHOICES = [(FEED, "Feed"), (STORY, "Story")]

    joke = models.ForeignKey(
        Joke, on_delete=models.CASCADE, related_name="instagram_shares"
    )
    kind = models.CharField(max_length=8, choices=KIND_CHOICES)
    media_pk = models.CharField(max_length=64)
    is_backfill = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["joke", "kind"], name="unique_joke_share_per_kind"
            )
        ]
        indexes = [models.Index(fields=["posted_at"])]

    def __str__(self):
        return f"{self.kind} share of joke {self.joke_id} ({self.media_pk})"
