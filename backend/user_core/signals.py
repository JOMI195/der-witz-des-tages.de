from django.db.models.signals import pre_delete
from django.dispatch import receiver
from joke_newsletter.models import NewsletterReciever
from .models import User


@receiver(pre_delete, sender=User)
def delete_newsletter_reciever_on_user_delete(sender, instance, **kwargs):
    """Delete the NewsletterReciever instance if email matches the User email before deletion."""
    # Find the NewsletterReciever with the same email as the User
    try:
        recipient = NewsletterReciever.objects.get(email=instance.email)
        recipient.delete()
    except NewsletterReciever.DoesNotExist:
        pass
