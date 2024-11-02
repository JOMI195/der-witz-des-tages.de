from datetime import date
import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from django.core.exceptions import ObjectDoesNotExist

from jokes.joke_of_the_day.joke_of_the_day import get_latest_joke_of_the_day
from jokes.models import JokeOfTheDay, ShareableImage
from socials_sharing.instagram.session import InstagramSessionHandler


def login_user_to_instagram():
    """
    Attempts to login to Instagram using either the cached session
    or the provided username and password from Django settings.

    Returns:
        Client: Authenticated Instagram client instance

    Raises:
        Exception: If login fails with both session and credentials
    """
    # Get credentials from Django settings
    INSTAGRAM_USERNAME = os.environ.get("INSTAGRAM_USERNAME", None)
    INSTAGRAM_PASSWORD = os.environ.get("INSTAGRAM_PASSWORD", None)

    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        raise Exception("Instagram credentials not configured in Django settings")

    cl = Client()
    cl.delay_range = [1, 3]

    session = InstagramSessionHandler.get_cached_session()
    login_via_session = False
    login_via_pw = False

    # Try to login via cached session first
    if session:
        try:
            cl.set_settings(session)
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

            # Verify session validity
            try:
                cl.get_timeline_feed()
                login_via_session = True
                print("Successfully logged in via cached session")
            except LoginRequired:
                print("Session is invalid, need to login via username and password")
                # Save device UUIDs for consistent device fingerprint
                old_session = cl.get_settings()
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                login_via_session = True
                # Cache the new session
                InstagramSessionHandler.save_cached_session(cl.get_settings())

        except Exception as e:
            print(f"Couldn't login user using cached session: {e}")

    # Try to login via username/password if session login failed
    if not login_via_session:
        try:
            print(
                f"Attempting to login via username and password. Username: {INSTAGRAM_USERNAME}"
            )
            if cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD):
                login_via_pw = True
                print("Successfully logged in via username/password")
                # Cache the new session
                InstagramSessionHandler.save_cached_session(cl.get_settings())
                print("Saved session to cache")
        except Exception as e:
            print(f"Couldn't login user using username and password: {e}")

    if not (login_via_pw or login_via_session):
        raise Exception("Couldn't login user with either password or session")

    return cl


def upload_shareable_image(client: Client):
    """
    Shares the shareable image on Instagram.
    """
    try:
        latest_joke_of_the_day: JokeOfTheDay = get_latest_joke_of_the_day()
        related_shareable_image: ShareableImage = (
            latest_joke_of_the_day.joke.shareable_image
        )
    except ObjectDoesNotExist as e:
        print(f"Failed to get images from db: {e}")

    today = date.today().strftime("%d.%m.%Y")

    hashtags = "#witzdestages #derwitzdestages #flachwitze #flachwitzfreitag #witze #bestewitze #witzegalerie #lustigewitze #deutschewitze #witzearmy #witzenhausen #jokes #memes #funny #comedy #lol #memesdaily #humor #fun #joke #instagram #follow #haha"

    feed_image_caption = (
        f"\nDer Witz des Tages vom {today} 😂\n\n"
        f"Besuche auch unsere Website www.der-witz-des-tages.de (Link in der Bio) für weitere tolle Features ✨:\n\n"
        f"👥 Reiche deinen Lieblingswitz ein und zeige der Welt wie lustig du bist!\n"
        f"📬 Abonniere unseren Email-Newsletter um tägliche Witze direkt in dein Postfach zu erhalten!\n\n"
        f"{hashtags}"
    ).strip()

    accessibility_text = (
        f"An image featuring the joke of the day from the date {today}. "
        f"The joke of the day is: {latest_joke_of_the_day.joke.text} and is printed on the bottom of the image. "
        f"In the center is an illustration that highlights the joke of the day. "
        f"Visit www.der-witz-des-tages.de for more jokes and information!"
    ).strip()

    if len(feed_image_caption) > 2200:
        raise ValueError("Caption exceeds Instagram's 2200 character limit")

    try:
        feed_media = client.photo_upload(
            path=related_shareable_image.image.path,
            caption=feed_image_caption,
            extra_data={
                "custom_accessibility_caption": accessibility_text,
            },
        )

        if not feed_media or not hasattr(feed_media, "id"):
            raise Exception(
                "Upload to feed appeared to succeed but no media object was returned"
            )

    except Exception as e:
        print(f"Failed to upload shareable image to feed: {e}")

    try:
        story_media = client.photo_upload_to_story(
            path=related_shareable_image.image.path,
            extra_data={
                "custom_accessibility_caption": accessibility_text,
            },
        )

        if not story_media or not hasattr(story_media, "id"):
            raise Exception(
                "Upload to story appeared to succeed but no media object was returned"
            )

        print(f"Successfully uploaded image to feed and story.")

    except Exception as e:
        print(f"Failed to upload shareable image to story: {e}")


def share_on_instagramm():
    try:
        client = login_user_to_instagram()
        upload_shareable_image(client)

    except Exception as e:
        print(f"Error: {e}")
