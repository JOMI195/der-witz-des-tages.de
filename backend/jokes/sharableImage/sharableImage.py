from jokes.models import ShareableImage, Joke, get_shareable_image_upload_path
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction


def save_shareable_image_to_model(joke: Joke, image_data: bytes) -> ShareableImage:
    with transaction.atomic():
        temp_shareable_image = ShareableImage(joke=joke)
        temp_filename = f"temp_joke_{joke.id}.jpg"
        full_path = get_shareable_image_upload_path(temp_shareable_image, temp_filename)
        image_file = ContentFile(image_data, name=os.path.basename(full_path))
        shareable_image, created = ShareableImage.objects.get_or_create(joke=joke)

        # If updating an existing image, delete the old one
        if not created and shareable_image.image:
            old_path = shareable_image.image.path
            default_storage.delete(old_path)

            # Remove the empty directory if it exists
            old_dir = os.path.dirname(old_path)
            if os.path.exists(old_dir) and not os.listdir(old_dir):
                os.rmdir(old_dir)

        # Save the new image
        shareable_image.image.save(image_file.name, image_file, save=True)

        return shareable_image
