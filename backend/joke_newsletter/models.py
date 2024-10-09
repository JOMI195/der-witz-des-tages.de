import uuid
from django.db import models


class NewsletterReciever(models.Model):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    activation_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    def __str__(self):
        return self.email
