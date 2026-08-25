from django.core.cache import cache
from instagrapi import Client

CACHE_KEY = "instagram_session"
CACHE_TIMEOUT = 60 * 60 * 24 * 30


class InstagramSessionHandler:
    """
    Handles Instagram authentication and session management for Django applications.
    """

    @staticmethod
    def get_cached_session():
        """Retrieve Instagram session from Django cache, unless it is outdated"""
        session = cache.get(CACHE_KEY)
        if not session:
            return None

        # A session pins the device fingerprint it was created with. Instagram
        # answers outdated app versions with HTTP 467 on every authenticated
        # endpoint, so a session from an older instagrapi must not be restored.
        cached_app_version = (session.get("device_settings") or {}).get("app_version")
        if cached_app_version != Client().device_settings["app_version"]:
            cache.delete(CACHE_KEY)
            return None

        return session

    @staticmethod
    def save_cached_session(session_data):
        """Save Instagram session to Django cache with expiration"""
        cache.set(CACHE_KEY, session_data, timeout=CACHE_TIMEOUT)
