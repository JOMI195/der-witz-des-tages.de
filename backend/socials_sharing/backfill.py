import logging
from datetime import date, timedelta

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from django.utils import timezone
from instagrapi.exceptions import ChallengeRequired

from jokes.models import JokeOfTheDay
from socials_sharing.instagram.instagram import (
    login_user_to_instagram,
    upload_to_feed,
)
from socials_sharing.models import InstagramShare

logger = logging.getLogger(__name__)

COOLDOWN_CACHE_KEY = "instagram_backfill_cooldown"
GENERIC_COOLDOWN_HOURS = 24
CHALLENGE_COOLDOWN_HOURS = 48

# The account was dormant for seven months, so the drip starts at one post a day
# and only widens once Instagram has tolerated the previous step.
RAMP = [(7, 1), (14, 2)]
MAX_DAILY_POSTS = 3


def backfill_since() -> date:
    return settings.INSTAGRAM_BACKFILL_SINCE


def candidates(since: date = None) -> QuerySet:
    """Missed jokes of the day that still have their image, newest first."""
    return (
        JokeOfTheDay.objects.filter(
            created_at__date__gte=since or backfill_since(),
            joke__shareable_image__isnull=False,
        )
        .exclude(joke__instagram_shares__kind=InstagramShare.FEED)
        .select_related("joke", "joke__shareable_image")
        .order_by("-created_at")
    )


def daily_cap() -> int:
    """Posts per day, widening with the age of the backfill."""
    first = (
        InstagramShare.objects.filter(is_backfill=True).order_by("posted_at").first()
    )
    if first is None:
        return RAMP[0][1]

    running_for = (timezone.now() - first.posted_at).days
    for days, cap in RAMP:
        if running_for < days:
            return cap

    return MAX_DAILY_POSTS


def posted_last_24h() -> int:
    return InstagramShare.objects.filter(
        is_backfill=True,
        kind=InstagramShare.FEED,
        posted_at__gte=timezone.now() - timedelta(hours=24),
    ).count()


def remaining_budget() -> int:
    return max(daily_cap() - posted_last_24h(), 0)


def in_cooldown() -> bool:
    return cache.get(COOLDOWN_CACHE_KEY) is not None


def start_cooldown(hours: int = GENERIC_COOLDOWN_HOURS) -> None:
    """Pause the backfill after a failure instead of hammering Instagram."""
    until = timezone.now() + timedelta(hours=hours)
    cache.set(COOLDOWN_CACHE_KEY, until.isoformat(), timeout=hours * 60 * 60)
    logger.warning("Instagram backfill paused until %s", until.isoformat())


def cooldown_until() -> str:
    return cache.get(COOLDOWN_CACHE_KEY)


def post_next(since: date = None, ignore_cap: bool = False, client=None) -> dict:
    """
    Posts the newest missing joke of the day to the feed, if the budget allows.

    Raises:
        Exception: If the upload fails, after putting the backfill on cooldown
    """
    if in_cooldown():
        return {"skipped": "cooldown", "until": cooldown_until()}

    if not ignore_cap and remaining_budget() <= 0:
        return {"skipped": "budget spent", "cap": daily_cap()}

    joke_of_the_day = candidates(since).first()
    if joke_of_the_day is None:
        return {"skipped": "nothing to post"}

    client = client or login_user_to_instagram()

    try:
        media = upload_to_feed(client, joke_of_the_day, is_backfill=True)
    except Exception as e:
        start_cooldown(
            CHALLENGE_COOLDOWN_HOURS
            if isinstance(e, ChallengeRequired)
            else GENERIC_COOLDOWN_HOURS
        )
        raise

    return {
        "joke_id": joke_of_the_day.joke_id,
        "day": timezone.localtime(joke_of_the_day.created_at).date().isoformat(),
        "media_pk": str(media.pk),
        "remaining": candidates(since).count(),
    }
