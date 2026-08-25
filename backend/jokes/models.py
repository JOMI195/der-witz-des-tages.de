import os
import uuid
from django.conf import settings
from django.db import models, transaction
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator
from jokes.joke_picture.variants import delete_variants


def discard_image_file(image_name: str, with_variants: bool = True) -> None:
    """
    Removes a stored image, its variants and the obfuscated directory it owned.

    Safe to call twice. Only ever call it through transaction.on_commit: a file
    deleted inside a transaction that later rolls back is gone for good.
    """
    if not image_name:
        return

    if with_variants:
        delete_variants(image_name)

    if default_storage.exists(image_name):
        default_storage.delete(image_name)

    directory = os.path.dirname(default_storage.path(image_name))
    if os.path.isdir(directory) and not os.listdir(directory):
        try:
            os.rmdir(directory)
        except OSError:
            pass


def _replaced_image_name(model, instance) -> str:
    """
    The stored name this save is about to overwrite.

    Reads the raw column instead of building a FieldFile, so a row that carries no
    file yet - the state get_or_create leaves behind - cannot raise here.
    """
    if not instance.pk:
        return ""

    stored_name = (
        model.objects.filter(pk=instance.pk).values_list("image", flat=True).first()
        or ""
    )
    return stored_name if stored_name != instance.image.name else ""


class Joke(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    joke_of_the_day_selection_weight = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Weight for Joke of the Day selection (1-100). Higher values increase selection probability.",
    )

    def __str__(self):
        return self.text[:50]


def get_joke_picture_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    obfuscated_dirname = str(uuid.uuid4())
    return os.path.join(
        "joke_pictures", obfuscated_dirname, f"joke_{instance.joke.id}{ext}"
    )


class JokePicture(models.Model):
    joke = models.OneToOneField(
        Joke, on_delete=models.CASCADE, related_name="joke_picture"
    )
    image = models.ImageField(upload_to=get_joke_picture_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture for Joke ID {self.joke.id}"

    def save(self, *args, **kwargs):
        replaced_name = _replaced_image_name(JokePicture, self)

        super().save(*args, **kwargs)

        if replaced_name:
            transaction.on_commit(lambda: discard_image_file(replaced_name))

    def delete(self, *args, **kwargs):
        image_name = self.image.name

        super().delete(*args, **kwargs)

        if image_name:
            transaction.on_commit(lambda: discard_image_file(image_name))


def get_shareable_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    obfuscated_dirname = str(uuid.uuid4())
    return os.path.join(
        "shareable_images", obfuscated_dirname, f"shareable_{instance.joke.id}{ext}"
    )


class ShareableImage(models.Model):
    joke = models.OneToOneField(
        Joke, on_delete=models.CASCADE, related_name="shareable_image"
    )
    image = models.ImageField(upload_to=get_shareable_image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shareable Image for Joke ID {self.joke.id}"

    def save(self, *args, **kwargs):
        replaced_name = _replaced_image_name(ShareableImage, self)

        super().save(*args, **kwargs)

        if replaced_name:
            transaction.on_commit(
                lambda: discard_image_file(replaced_name, with_variants=False)
            )

    def delete(self, *args, **kwargs):
        image_name = self.image.name

        super().delete(*args, **kwargs)

        if image_name:
            transaction.on_commit(
                lambda: discard_image_file(image_name, with_variants=False)
            )


class JokeOfTheDay(models.Model):
    joke = models.ForeignKey(
        Joke, on_delete=models.CASCADE, related_name="joke_of_the_day"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class SubmittedJoke(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]
