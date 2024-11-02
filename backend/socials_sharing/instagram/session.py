from django.core.cache import cache


class InstagramSessionHandler:
    """
    Handles Instagram authentication and session management for Django applications.
    """

    @staticmethod
    def get_cached_session():
        """Retrieve Instagram session from Django cache"""
        return cache.get("instagram_session")

    @staticmethod
    def save_cached_session(session_data):
        """Save Instagram session to Django cache with expiration"""
        # Cache for 30 days (or adjust as needed)
        cache.set("instagram_session", session_data, timeout=60 * 60 * 24 * 30)
