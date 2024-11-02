from typing import Dict
from config.celery import celery
from random import choice
from django.core.exceptions import ObjectDoesNotExist
from jokes.sharableImage.screenshot import capture_screenshot
from jokes.sharableImage.template import get_shareable_image_html_template
from jokes.sharableImage.sharableImage import save_shareable_image_to_model
from jokes.models import Joke, JokePicture
from jokes.joke_of_the_day.joke_of_the_day import (
    create_joke_of_the_day_entry,
    get_joke_of_the_day,
    get_latest_joke_of_the_day,
)
from jokes.joke_picture.joke_picture import get_or_create_joke_picture


@celery.task
def create_joke_picture(joke_data) -> Dict[str, int]:
    joke_id = joke_data["joke_id"]
    joke = Joke.objects.get(id=joke_id)
    joke_picture = get_or_create_joke_picture(joke=joke)
    return {"joke_id": joke.id}


@celery.task
def select_joke_of_the_day() -> Dict[str, int]:
    joke = get_joke_of_the_day()
    create_joke_of_the_day_entry(joke)
    return {"joke_id": joke.id}


@celery.task
def get_allready_created_joke_of_the_day() -> Dict[str, int]:
    jokes_with_pictures = Joke.objects.filter(joke_picture__isnull=False)

    if not jokes_with_pictures.exists():
        raise ValueError("No jokes with pictures available.")

    random_joke = choice(jokes_with_pictures)

    try:
        joke_picture = random_joke.joke_picture
    except ObjectDoesNotExist:
        raise ValueError("Selected joke does not have an associated picture.")

    return {"joke_id": random_joke.id}


@celery.task
def create_shareable_image(*args, **kwargs):
    latest_joke_of_the_day: Joke = get_latest_joke_of_the_day()
    related_joke_picture: JokePicture = latest_joke_of_the_day.joke.joke_picture

    html_content = get_shareable_image_html_template(
        joke=latest_joke_of_the_day.joke, image_field=related_joke_picture.image
    )

    image_data = capture_screenshot(html_content)

    shareable_image = save_shareable_image_to_model(
        joke=latest_joke_of_the_day.joke, image_data=image_data
    )

    return f"{shareable_image} saved to {shareable_image.image.path}"
