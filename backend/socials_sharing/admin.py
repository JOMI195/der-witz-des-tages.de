from django.contrib import admin

from .models import InstagramShare


@admin.register(InstagramShare)
class InstagramShareAdmin(admin.ModelAdmin):
    list_display = ("id", "joke", "kind", "media_pk", "is_backfill", "posted_at")
    list_filter = ("kind", "is_backfill", "posted_at")
    search_fields = ("media_pk", "joke__text")
    list_per_page = 50
    ordering = ("-posted_at",)
