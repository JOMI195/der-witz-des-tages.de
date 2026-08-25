from django.core.files.base import ContentFile
from django.db import transaction

from jokes.joke_picture.image import generate_image_content
from jokes.joke_picture.prompt import generateJokePicturePrompt
from jokes.joke_picture.variants import generate_variants
from jokes.models import Joke, JokePicture, discard_image_file


def get_or_create_joke_picture(joke: Joke) -> JokePicture:
    prompt = generateJokePicturePrompt(joke.text)
    image_data = generate_image_content(promptContent=prompt)
    joke_picture = save_image_to_model(joke=joke, image_data=image_data)
    return joke_picture


def save_image_to_model(joke: Joke, image_data: bytes) -> JokePicture:
    # only the extension survives, upload_to rebuilds the whole path
    image_file = ContentFile(image_data, name=f"joke_{joke.id}.jpg")

    with transaction.atomic():
        joke_picture, _ = JokePicture.objects.get_or_create(joke=joke)
        previous_name = joke_picture.image.name

        try:
            joke_picture.image.save(image_file.name, image_file, save=True)
            generate_variants(joke_picture.image)
        except Exception:
            # the file reaches storage before the row is written, so a rollback
            # would leave it behind
            if joke_picture.image.name != previous_name:
                discard_image_file(joke_picture.image.name)
            raise

    return joke_picture
