from django.contrib import admin

from .models import NewsletterReciever


@admin.register(NewsletterReciever)
class NewsletterRecieverAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_active")
    search_fields = ("email",)
    list_filter = ("email", "subscribed_at", "is_active")
    list_per_page = 50
    ordering = ("subscribed_at",)

    readonly_fields = ("subscribed_at", "unsubscribe_token", "activation_token")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "is_active",
                    "subscribed_at",
                    "unsubscribe_token",
                    "activation_token",
                )
            },
        ),
    )
