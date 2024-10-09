import os
from django.conf import settings
from appEmail.tasks import send_django_mail_with_logo

from .models import NewsletterReciever


def send_newsletter_reciever_activation_email(reciever: NewsletterReciever):
    activation_link = os.environ.get(
        "FRONTEND_BASE_URL"
    ) + settings.FRONTEND_NEWSLETTER_RECIEVER_ACTIVATION_URL.format(
        activation_token=reciever.activation_token
    )

    context = {
        "subject": "Aktiviere den Erhalt des Der-Witz-des-Tages Newsletters",
        "activation_link": activation_link,
        "reciever": reciever,
    }
    template_name = "joke_newsletter/newsletter_activation.html"
    send_django_mail_with_logo(
        template_name=template_name,
        context=context,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=[reciever.email],
    )


def send_newsletter_reciever_confirmation_email(reciever: NewsletterReciever):
    context = {
        "subject": "Du bist jetzt ein Teil des Der-Witz-des-Tages Newsletters. Viel Spaß mit den Witzen!",
        "reciever": reciever,
        "home_link": os.environ.get("FRONTEND_BASE_URL"),
    }
    template_name = "joke_newsletter/newsletter_confirmation.html"
    send_django_mail_with_logo(
        template_name=template_name,
        context=context,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=[reciever.email],
    )
