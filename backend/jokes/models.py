import os
import uuid
from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator
from jokes.joke_picture.variants import delete_variants, variant_names


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
        if self.pk:
            try:
                old_instance = JokePicture.objects.get(pk=self.pk)
                if old_instance.image != self.image:
                    old_dir = os.path.dirname(old_instance.image.path)
                    delete_variants(old_instance.image)
                    old_instance.image.delete(save=False)
                    # every upload gets its own obfuscated directory, so the old
                    # one is empty now and would linger otherwise
                    if os.path.isdir(old_dir) and not os.listdir(old_dir):
                        os.rmdir(old_dir)
            except JokePicture.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            dir_path = os.path.dirname(image_path)
            variant_paths = [
                os.path.join(settings.MEDIA_ROOT, name) for name in variant_names(self.image.name)
            ]
            delete_variants(self.image)
        else:
            image_path = None
            dir_path = None
            variant_paths = []

        super().delete(*args, **kwargs)

        if image_path and os.path.isfile(image_path):
            default_storage.delete(image_path)

        # A variant that survived the storage delete would keep the directory alive
        for variant_path in variant_paths:
            if os.path.isfile(variant_path):
                os.remove(variant_path)

        if dir_path and os.path.exists(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)


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
        if self.pk:
            try:
                old_instance = ShareableImage.objects.get(pk=self.pk)
                if old_instance.image != self.image:
                    old_instance.image.delete(save=False)
            except ShareableImage.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            dir_path = os.path.dirname(image_path)
        else:
            image_path = None
            dir_path = None

        super().delete(*args, **kwargs)

        if image_path and os.path.isfile(image_path):
            default_storage.delete(image_path)
        if dir_path and os.path.exists(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)


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
