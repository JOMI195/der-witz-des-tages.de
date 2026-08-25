import random

from django.conf import settings

from config.celery import celery
from socials_sharing import backfill
from socials_sharing.instagram.instagram import share_on_instagramm


@celery.task
def share_on_socials(*args, **kwargs):
    share_on_instagramm()


@celery.task
def share_on_socials_instagram(*args, **kwargs):
    share_on_instagramm()


@celery.task
def backfill_instagram_feed(*args, **kwargs):
    """
    Posts one missed joke of the day to the feed, rate limited by socials_sharing.backfill.

    Beat fires this in a few fixed slots; the jitter keeps the posts off a
    round-number schedule and the budget check makes the surplus slots no-ops.
    """
    if not settings.PRODUCTION:
        return {"skipped": "not production"}

    return backfill.post_next()


@celery.task
def dispatch_instagram_backfill(*args, **kwargs):
    if not settings.PRODUCTION:
        return {"skipped": "not production"}

    if backfill.in_cooldown() or backfill.remaining_budget() <= 0:
        return {"skipped": "nothing scheduled"}

    countdown = random.randint(0, 45 * 60)
    backfill_instagram_feed.apply_async(countdown=countdown)

    return {"scheduled_in_seconds": countdown}
