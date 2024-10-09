from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_accounts.models import Account
from .models import NewsletterReciever


@receiver(post_save, sender=NewsletterReciever)
def handle_newsletter_reciever_create(sender, instance, **kwargs):
    try:
        account = Account.objects.get(user__email=instance.email)
        if instance.is_active:
            account.recieves_newsletter = True
            account.save()
    except Account.DoesNotExist:
        pass


@receiver(post_delete, sender=NewsletterReciever)
def handle_newsletter_reciever_delete(sender, instance, **kwargs):
    try:
        account = Account.objects.get(user__email=instance.email)
        account.recieves_newsletter = False
        account.save()
    except Account.DoesNotExist:
        pass
