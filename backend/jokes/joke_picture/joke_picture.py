import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from jokes.models import Joke, JokePicture, get_joke_picture_upload_path
from jokes.joke_picture.image import generate_image_content
from jokes.joke_picture.prompt import generateJokePicturePrompt
from jokes.models import Joke, JokePicture
from django.db import transaction


def get_or_create_joke_picture(joke: Joke) -> JokePicture:
    prompt = generateJokePicturePrompt(joke.text)
    image_data = generate_image_content(promptContent=prompt)
    joke_picture = save_image_to_model(joke=joke, image_data=image_data)
    return joke_picture


def save_image_to_model(joke: Joke, image_data: bytes) -> JokePicture:
    with transaction.atomic():
        temp_joke_picture = JokePicture(joke=joke)
        temp_filename = f"temp_joke_{joke.id}.jpg"
        full_path = get_joke_picture_upload_path(temp_joke_picture, temp_filename)
        image_file = ContentFile(image_data, name=os.path.basename(full_path))
        joke_picture, created = JokePicture.objects.get_or_create(joke=joke)

        # If updating an existing image, delete the old one
        if not created and joke_picture.image:
            old_path = joke_picture.image.path
            default_storage.delete(old_path)

            # Remove the empty directory if it exists
            old_dir = os.path.dirname(old_path)
            if os.path.exists(old_dir) and not os.listdir(old_dir):
                os.rmdir(old_dir)

        # Save the new image
        joke_picture.image.save(image_file.name, image_file, save=True)

        return joke_picture
