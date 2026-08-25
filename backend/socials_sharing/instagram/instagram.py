import logging
import os

from django.utils import timezone
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

from jokes.joke_of_the_day.joke_of_the_day import get_latest_joke_of_the_day
from jokes.models import JokeOfTheDay, ShareableImage
from socials_sharing.instagram.session import InstagramSessionHandler
from socials_sharing.models import InstagramShare

logger = logging.getLogger(__name__)

HASHTAGS = "#witzdestages #derwitzdestages #flachwitze #flachwitzfreitag #witze #bestewitze #witzegalerie #lustigewitze #deutschewitze #witzearmy #witzenhausen #jokes #memes #funny #comedy #lol #memesdaily #humor #fun #joke #instagram #follow #haha"

CAPTION_MAX_LENGTH = 2200


def login_user_to_instagram() -> Client:
    """
    Login to Instagram, preferring the cached session over the credentials.

    Returns:
        Client: Authenticated Instagram client instance

    Raises:
        Exception: If login fails with both session and credentials
    """
    username = os.environ.get("INSTAGRAM_USERNAME")
    password = os.environ.get("INSTAGRAM_PASSWORD")

    if not username or not password:
        raise Exception("Instagram credentials not configured")

    client = Client()
    client.delay_range = [1, 3]

    session = InstagramSessionHandler.get_cached_session()

    if session:
        try:
            client.set_settings(session)
            client.login(username, password)
            client.get_timeline_feed()
            logger.info("Logged in to Instagram via cached session")
            InstagramSessionHandler.save_cached_session(client.get_settings())
            return client
        except LoginRequired:
            logger.info("Cached Instagram session expired, logging in with credentials")
            # Keep the device fingerprint, Instagram distrusts a new one.
            uuids = client.get_settings()["uuids"]
            client.set_settings({})
            client.set_uuids(uuids)
        except Exception as e:
            logger.warning("Login via cached Instagram session failed: %s", e)
            client = Client()
            client.delay_range = [1, 3]

    client.login(username, password)
    client.get_timeline_feed()
    logger.info("Logged in to Instagram as %s via credentials", username)
    InstagramSessionHandler.save_cached_session(client.get_settings())

    return client


def joke_of_the_day_date(joke_of_the_day: JokeOfTheDay) -> str:
    """The day the joke was picked for, which is not today for a backfilled post."""
    return timezone.localtime(joke_of_the_day.created_at).strftime("%d.%m.%Y")


def build_caption(day: str) -> str:
    caption = (
        f"\nDer Witz des Tages vom {day} 😂\n\n"
        f"Besuche auch unsere Website www.der-witz-des-tages.de (Link in der Bio) für weitere tolle Features ✨:\n\n"
        f"👥 Reiche deinen Lieblingswitz ein und zeige der Welt wie lustig du bist!\n"
        f"📬 Abonniere unseren Email-Newsletter um tägliche Witze direkt in dein Postfach zu erhalten!\n\n"
        f"{HASHTAGS}"
    ).strip()

    if len(caption) > CAPTION_MAX_LENGTH:
        raise ValueError(
            f"Caption exceeds Instagram's {CAPTION_MAX_LENGTH} character limit"
        )

    return caption


def build_accessibility_text(joke_text: str, day: str) -> str:
    return (
        f"An image featuring the joke of the day from the date {day}. "
        f"The joke of the day is: {joke_text} and is printed on the bottom of the image. "
        f"In the center is an illustration that highlights the joke of the day. "
        f"Visit www.der-witz-des-tages.de for more jokes and information!"
    ).strip()


def get_shareable_image(joke_of_the_day: JokeOfTheDay) -> ShareableImage:
    """
    Raises:
        Exception: If the joke has no shareable image or the file is gone
    """
    shareable_image: ShareableImage = getattr(
        joke_of_the_day.joke, "shareable_image", None
    )
    if shareable_image is None or not shareable_image.image:
        raise Exception(f"Joke of the day {joke_of_the_day.pk} has no shareable image")

    if not os.path.exists(shareable_image.image.path):
        raise Exception(
            f"Shareable image file for joke of the day {joke_of_the_day.pk} is missing: "
            f"{shareable_image.image.name}"
        )

    return shareable_image


def upload_to_feed(
    client: Client, joke_of_the_day: JokeOfTheDay, is_backfill: bool = False
):
    """
    Uploads the shareable image to the feed and records it in the ledger.

    Raises:
        Exception: If the upload fails or Instagram returns no media
    """
    shareable_image = get_shareable_image(joke_of_the_day)
    day = joke_of_the_day_date(joke_of_the_day)

    media = client.photo_upload(
        path=shareable_image.image.path,
        caption=build_caption(day),
        extra_data={
            "custom_accessibility_caption": build_accessibility_text(
                joke_of_the_day.joke.text, day
            )
        },
    )

    if not getattr(media, "pk", None):
        raise Exception("Upload to feed returned no media object")

    InstagramShare.objects.create(
        joke=joke_of_the_day.joke,
        kind=InstagramShare.FEED,
        media_pk=str(media.pk),
        is_backfill=is_backfill,
    )
    logger.info("Uploaded joke %s to feed (%s)", joke_of_the_day.joke_id, media.pk)

    return media


def upload_to_story(client: Client, joke_of_the_day: JokeOfTheDay):
    """
    Uploads the shareable image as a story and records it in the ledger.

    Raises:
        Exception: If the upload fails or Instagram returns no media
    """
    shareable_image = get_shareable_image(joke_of_the_day)
    day = joke_of_the_day_date(joke_of_the_day)

    media = client.photo_upload_to_story(
        path=shareable_image.image.path,
        extra_data={
            "custom_accessibility_caption": build_accessibility_text(
                joke_of_the_day.joke.text, day
            )
        },
    )

    if not getattr(media, "pk", None):
        raise Exception("Upload to story returned no media object")

    InstagramShare.objects.update_or_create(
        joke=joke_of_the_day.joke,
        kind=InstagramShare.STORY,
        defaults={"media_pk": str(media.pk)},
    )
    logger.info("Uploaded joke %s to story (%s)", joke_of_the_day.joke_id, media.pk)

    return media


def upload_shareable_image(client: Client) -> None:
    """
    Shares the latest joke of the day on Instagram, in the feed and as a story.

    Raises:
        Exception: If there is nothing to share or either upload fails
    """
    latest_joke_of_the_day: JokeOfTheDay = get_latest_joke_of_the_day()
    if latest_joke_of_the_day is None:
        raise Exception("No joke of the day exists, nothing to share")

    failures = []

    try:
        upload_to_feed(client, latest_joke_of_the_day)
    except Exception as e:
        logger.exception("Failed to upload shareable image to feed")
        failures.append(f"feed: {e}")

    try:
        upload_to_story(client, latest_joke_of_the_day)
    except Exception as e:
        logger.exception("Failed to upload shareable image to story")
        failures.append(f"story: {e}")

    if failures:
        raise Exception(f"Instagram upload failed for {', '.join(failures)}")


def share_on_instagramm() -> None:
    client = login_user_to_instagram()
    upload_shareable_image(client)
