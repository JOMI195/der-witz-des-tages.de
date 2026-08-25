from django.core.files.base import ContentFile
from django.db import transaction

from jokes.models import Joke, ShareableImage, discard_image_file


def save_shareable_image_to_model(joke: Joke, image_data: bytes) -> ShareableImage:
    # only the extension survives, upload_to rebuilds the whole path
    image_file = ContentFile(image_data, name=f"shareable_{joke.id}.jpg")

    with transaction.atomic():
        shareable_image, _ = ShareableImage.objects.get_or_create(joke=joke)
        previous_name = shareable_image.image.name

        try:
            shareable_image.image.save(image_file.name, image_file, save=True)
        except Exception:
            # the file reaches storage before the row is written, so a rollback
            # would leave it behind
            if shareable_image.image.name != previous_name:
                discard_image_file(shareable_image.image.name, with_variants=False)
            raise

    return shareable_image
