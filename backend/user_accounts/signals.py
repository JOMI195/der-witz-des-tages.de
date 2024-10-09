from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from joke_newsletter.models import NewsletterReciever
from .models import Account


@receiver(post_save, sender=Account)
def manage_newsletter_subscription(sender, instance, created, **kwargs):
    if created:
        try:
            reciever = NewsletterReciever.objects.get(email=instance.user.email)
            if reciever.is_active:
                instance.recieves_newsletter = True
                instance.save()
        except NewsletterReciever.DoesNotExist:
            pass
    else:
        if instance.recieves_newsletter:
            reciever = NewsletterReciever.objects.get_or_create(
                email=instance.user.email
            )[0]
            if reciever.is_active == False:
                reciever.is_active = True
                reciever.save()
        else:
            NewsletterReciever.objects.filter(email=instance.user.email).delete()


@receiver(post_delete, sender=Account)
def delete_newsletter_subscription(sender, instance, **kwargs):
    NewsletterReciever.objects.filter(email=instance.user.email).delete()
