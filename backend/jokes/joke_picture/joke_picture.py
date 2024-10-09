from jokes.joke_picture.image import generate_image_content, save_image_to_model
from jokes.joke_picture.prompt import generateJokePicturePrompt
from jokes.models import Joke, JokePicture


def get_or_create_joke_picture(joke: Joke) -> JokePicture:
    prompt = generateJokePicturePrompt(joke.text)
    image_data = generate_image_content(promptContent=prompt)
    joke_picture = save_image_to_model(joke=joke, image_data=image_data)
    return joke_picture
