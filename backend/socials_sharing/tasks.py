from config.celery import celery
from socials_sharing.instagram.instagram import share_on_instagramm


@celery.task
def share_on_socials(*args, **kwargs):
    share_on_instagramm()


@celery.task
def share_on_socials_instagram(*args, **kwargs):
    share_on_instagramm()
