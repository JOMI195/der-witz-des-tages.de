import os
import requests
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from jokes.models import Joke, JokePicture, get_upload_path


def generate_image_content(promptContent: str) -> bytes:
    API_KEY = os.environ.get("GETIMGAI_API_KEY")

    base_url = "https://api.getimg.ai/v1"

    generation_endpoint = "/essential-v2/text-to-image"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}",
        "content-Type": "application/json",
    }

    generation_data = {
        "prompt": "{promtContent}".format(promtContent=promptContent),
        "style": "art",
        "aspect_ratio": "1:1",
        "response_format": "b64",
        "output_format": "jpeg",
    }

    response_generation = requests.post(
        f"{base_url}{generation_endpoint}", headers=headers, json=generation_data
    )

    if response_generation.status_code == 200:
        generated_data = response_generation.json()
        generated_image_data = base64.b64decode(generated_data["image"])
        return generated_image_data
    else:
        raise ValueError(f"Error generating image: {response_generation.status_code}")


def save_image_to_model(joke: Joke, image_data: bytes) -> JokePicture:
    temp_joke_picture = JokePicture(joke=joke)
    temp_filename = f"temp_joke_{joke.id}.jpg"
    full_path = get_upload_path(temp_joke_picture, temp_filename)
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
