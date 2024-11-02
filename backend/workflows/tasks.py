from config.celery import celery
from celery import chain
from jokes.tasks import (
    create_joke_picture,
    create_shareable_image,
    get_allready_created_joke_of_the_day,
    select_joke_of_the_day,
)
from joke_newsletter.tasks import send_newsletter


@celery.task
def joke_of_the_day_full_workflow():
    chain(
        select_joke_of_the_day.s(),
        create_joke_picture.s(),
        send_newsletter.s(),
        create_shareable_image.s(),
    ).apply_async()


@celery.task
def joke_of_the_day_full_workflow_specific(recipient_emails):
    chain(
        select_joke_of_the_day.s(),
        create_joke_picture.s(),
        send_newsletter.s(recipient_emails=recipient_emails),
        create_shareable_image.s(),
    ).apply_async()


@celery.task
def joke_of_the_day_email_only_workflow_specific(recipient_emails):
    chain(
        get_allready_created_joke_of_the_day.s(),
        send_newsletter.s(recipient_emails=recipient_emails),
        create_shareable_image.s(),
    ).apply_async()
