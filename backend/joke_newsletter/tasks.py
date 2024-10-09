from copy import copy
from django.utils import timezone
from datetime import timedelta
from celery import chain
from django.conf import settings
from datetime import date
from celery import group
from celery.exceptions import SoftTimeLimitExceeded
import os
from django.core.exceptions import ObjectDoesNotExist
from appEmail.tasks import send_django_mail_with_logo
from jokes.models import Joke, JokePicture
from .models import NewsletterReciever
from jokes.tasks import (
    create_joke_picture,
    get_allready_created_joke_of_the_day,
    select_joke_of_the_day,
)
from config.celery import celery
from django.shortcuts import get_object_or_404


@celery.task(bind=True, max_retries=3, soft_time_limit=30)
def send_single_email(self, template_name, context, from_email, to_email, images):
    try:
        send_django_mail_with_logo(
            template_name=template_name,
            context=context,
            from_email=from_email,
            to_emails=[to_email],
            images=images,
        )
    except SoftTimeLimitExceeded:
        self.retry(countdown=10)


@celery.task
def send_newsletter(joke_data, recipient_emails=None, batch_delay=5):
    joke_id = joke_data["joke_id"]
    joke = get_object_or_404(Joke, pk=joke_id)

    try:
        joke_picture: JokePicture = joke.joke_picture
    except ObjectDoesNotExist:
        raise ValueError("Selected joke does not have an associated picture.")

    context = {
        "joke": joke.text,
        "date": date.today(),
        "username": (
            "Jomi" if joke.created_by.username == "admin" else joke.created_by.username
        ),
        "subject": "Dein Flach-/ Wortwitz des Tages",
    }

    if recipient_emails:
        subscribers = list(
            NewsletterReciever.objects.filter(
                email__in=recipient_emails, is_active=True
            )
        )
    else:
        subscribers = list(NewsletterReciever.objects.filter(is_active=True))

    subscriber_count = len(subscribers)

    batch_size = 10
    subscriber_batches = [
        subscribers[i : i + batch_size] for i in range(0, len(subscribers), batch_size)
    ]

    tasks = []
    for i, subscriber_batch in enumerate(subscriber_batches):
        email_tasks = []
        for subscriber in subscriber_batch:
            unsubscribe_link = os.environ.get(
                "FRONTEND_BASE_URL"
            ) + settings.FRONTEND_NEWSLETTER_RECIEVER_UNSUBSCRIBE_URL.format(
                unsubscribe_token=subscriber.unsubscribe_token
            )
            new_context = copy(context)
            new_context["unsubscribe_link"] = unsubscribe_link

            email_tasks.append(
                send_single_email.s(
                    template_name="joke_newsletter/joke_newsletter.html",
                    context=new_context,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_email=subscriber.email,
                    images=[
                        {
                            "path": joke_picture.image.path,
                            "cid": "joke_image",
                            "template_identifier": "joke_image_cid",
                            "filename": "witz-des-tages-illustration.jpg",
                        }
                    ],
                )
            )

        batch_task = group(email_tasks)
        tasks.append(batch_task.apply_async(countdown=i * batch_delay))

    return {
        "status": "Newsletter sending initiated",
        "subscriber_count": subscriber_count,
    }


@celery.task
def joke_of_the_day_full_workflow():
    chain(
        select_joke_of_the_day.s(), create_joke_picture.s(), send_newsletter.s()
    ).apply_async()


@celery.task
def joke_of_the_day_email_only_workflow():
    chain(get_allready_created_joke_of_the_day.s(), send_newsletter.s()).apply_async()


@celery.task
def joke_of_the_day_full_workflow_specific(recipient_emails):
    chain(
        select_joke_of_the_day.s(),
        create_joke_picture.s(),
        send_newsletter.s(recipient_emails=recipient_emails),
    ).apply_async()


@celery.task
def joke_of_the_day_email_only_workflow_specific(recipient_emails):
    chain(
        get_allready_created_joke_of_the_day.s(),
        send_newsletter.s(recipient_emails=recipient_emails),
    ).apply_async()


@celery.task
def delete_inactive_newsletter_recipients():
    """Delete newsletter recipients who haven't activated their account within 24 hours."""
    time_threshold = timezone.now() - timedelta(hours=24)
    inactive_recipients = NewsletterReciever.objects.filter(
        is_active=False, subscribed_at__lt=time_threshold
    )
    count = inactive_recipients.count()
    inactive_recipients.delete()
    return f"Deleted {count} inactive newsletter recipients."
