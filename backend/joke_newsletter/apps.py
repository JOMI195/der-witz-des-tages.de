from django.apps import AppConfig


class JokeNewsletterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "joke_newsletter"

    def ready(self):
        import joke_newsletter.signals
