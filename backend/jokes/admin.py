from django.contrib import admin
from .models import Joke, JokeOfTheDay, JokePicture, ShareableImage, SubmittedJoke
from django.utils.html import format_html
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "created_at",
        "created_by",
    )
    search_fields = ("text",)
    list_filter = (
        "created_at",
        "created_by",
        "joke_of_the_day_selection_weight",
    )
    list_per_page = 50
    ordering = ("-created_at",)

    def joke_picture_display(self, obj):
        if hasattr(obj, "joke_picture") and obj.joke_picture and obj.joke_picture.image:
            return format_html(
                '<img src="{}" width="200" height="200" />', obj.joke_picture.image.url
            )
        return "No picture created yet"

    def shareable_image_display(self, obj):
        if (
            hasattr(obj, "shareable_image")
            and obj.shareable_image
            and obj.shareable_image.image
        ):
            return format_html(
                '<img src="{}" width="200" height="200" />',
                obj.shareable_image.image.url,
            )
        return "No picture created yet"

    joke_picture_display.short_description = "Joke picture"
    shareable_image_display.short_description = "Shareable Image"

    readonly_fields = (
        "joke_picture_display",
        "shareable_image_display",
        "created_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text",
                    "created_at",
                    "created_by",
                    "joke_of_the_day_selection_weight",
                    "joke_picture_display",
                    "shareable_image_display",
                )
            },
        ),
    )


@admin.register(JokePicture)
class JokePictureAdmin(admin.ModelAdmin):
    list_display = ("id", "joke", "created_at")
    search_fields = ("joke__text",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def joke_picture_display(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" height="200" />', obj.image.url
            )
        return "Something went wrong - no picture"

    joke_picture_display.short_description = "Joke picture"

    readonly_fields = (
        "joke_picture_display",
        "created_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "joke",
                    "created_at",
                    "joke_picture_display",
                )
            },
        ),
    )


@admin.register(ShareableImage)
class ShareableImageAdmin(admin.ModelAdmin):
    list_display = ("id", "joke", "created_at")
    search_fields = ("joke__text",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def shareable_image_display(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" height="200" />', obj.image.url
            )
        return "Something went wrong - no picture"

    shareable_image_display.short_description = "Joke picture"

    readonly_fields = (
        "shareable_image_display",
        "created_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "joke",
                    "created_at",
                    "shareable_image_display",
                )
            },
        ),
    )


@admin.register(JokeOfTheDay)
class JokeOfTheDayAdmin(admin.ModelAdmin):
    list_display = ("id", "joke", "created_at")
    search_fields = (
        "joke",
        "created_at",
    )
    list_filter = ("created_at",)
    list_per_page = 50
    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "joke",
                    "created_at",
                )
            },
        ),
    )


@admin.register(SubmittedJoke)
class SubmittedJokeAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at", "created_by", "is_approved")
    search_fields = ("text",)
    list_filter = ("created_at", "created_by", "is_approved")
    list_per_page = 50
    ordering = ("-created_at",)
    actions = ["approve_joke"]

    readonly_fields = ("created_at", "is_approved")

    fieldsets = (
        (
            None,
            {"fields": ("text", "created_by", "created_at", "is_approved")},
        ),
    )

    def approve_joke(self, request, queryset):
        count = 0
        for joke in queryset:
            if not joke.is_approved:
                try:
                    joke.is_approved = True
                    joke.save()
                    count += 1
                except ValidationError as e:
                    self.message_user(request, str(e), level=messages.ERROR)
                    joke.is_approved = False
                    joke.save()
                    return

        self.message_user(
            request,
            _("Successfully approved {} jokes.".format(count)),
            messages.SUCCESS,
        )

    approve_joke.short_description = "Approve selected jokes"
