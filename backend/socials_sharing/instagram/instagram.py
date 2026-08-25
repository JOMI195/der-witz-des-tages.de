from datetime import date
import logging
import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

from jokes.joke_of_the_day.joke_of_the_day import get_latest_joke_of_the_day
from jokes.models import JokeOfTheDay, ShareableImage
from socials_sharing.instagram.session import InstagramSessionHandler

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


def build_caption(today: str) -> str:
    caption = (
        f"\nDer Witz des Tages vom {today} 😂\n\n"
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


def upload_shareable_image(client: Client) -> None:
    """
    Shares the shareable image on Instagram, in the feed and as a story.

    Raises:
        Exception: If the image is missing or either upload fails
    """
    latest_joke_of_the_day: JokeOfTheDay = get_latest_joke_of_the_day()
    if latest_joke_of_the_day is None:
        raise Exception("No joke of the day exists, nothing to share")

    shareable_image: ShareableImage = getattr(
        latest_joke_of_the_day.joke, "shareable_image", None
    )
    if shareable_image is None or not shareable_image.image:
        raise Exception(
            f"Joke of the day {latest_joke_of_the_day.pk} has no shareable image"
        )

    today = date.today().strftime("%d.%m.%Y")
    caption = build_caption(today)
    accessibility_text = (
        f"An image featuring the joke of the day from the date {today}. "
        f"The joke of the day is: {latest_joke_of_the_day.joke.text} and is printed on the bottom of the image. "
        f"In the center is an illustration that highlights the joke of the day. "
        f"Visit www.der-witz-des-tages.de for more jokes and information!"
    ).strip()

    image_path = shareable_image.image.path
    extra_data = {"custom_accessibility_caption": accessibility_text}

    failures = []

    try:
        feed_media = client.photo_upload(
            path=image_path, caption=caption, extra_data=extra_data
        )
        if not getattr(feed_media, "pk", None):
            raise Exception("No media object returned")
        logger.info("Uploaded shareable image to feed (%s)", feed_media.pk)
    except Exception as e:
        logger.exception("Failed to upload shareable image to feed")
        failures.append(f"feed: {e}")

    try:
        story_media = client.photo_upload_to_story(
            path=image_path, extra_data=extra_data
        )
        if not getattr(story_media, "pk", None):
            raise Exception("No media object returned")
        logger.info("Uploaded shareable image to story (%s)", story_media.pk)
    except Exception as e:
        logger.exception("Failed to upload shareable image to story")
        failures.append(f"story: {e}")

    if failures:
        raise Exception(f"Instagram upload failed for {', '.join(failures)}")


def share_on_instagramm() -> None:
    client = login_user_to_instagram()
    upload_shareable_image(client)
