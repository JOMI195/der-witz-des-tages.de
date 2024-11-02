import base64
import os
from random import random, uniform, choice
from typing import Optional, Tuple
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import ImageField
from jokes.models import Joke


def get_base64_image_from_imagefield(image_field: ImageField) -> str:
    with default_storage.open(image_field.name, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def get_base64_image_from_url(image_url: str) -> str:
    with open(image_url, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def get_shareable_image_html_template(joke: Joke, image_field: ImageField) -> str:

    img_rot, card_rot = get_random_rotations()
    color = get_random_color()

    html_content = generate_social_template(
        joke=joke.text,
        image_field=image_field,
        image_rotation=img_rot,
        card_rotation=card_rot,
        card_color=color,
    )

    return html_content


def get_random_rotations() -> Tuple[float, float]:
    """
    Generate random rotation values for the image and card.

    Returns:
        Tuple[float, float]: (image_rotation, card_rotation)
    """
    image_rotation = uniform(-3, -1)
    card_rotation = uniform(1, 3)

    if random() < 0.5:
        return card_rotation, image_rotation

    return image_rotation, card_rotation


def get_random_color(color_list: Optional[list] = None) -> str:
    """
    Select a random color from the provided list or default colors.

    Args:
        color_list (list, optional): List of colors to choose from

    Returns:
        str: Selected color
    """
    default_colors = [
        "#D5C8F4",
        "#F1E3C7",
        "#F2D7EC",
    ]
    colors = color_list if color_list is not None else default_colors
    return choice(colors)


def generate_social_template(
    joke: str,
    image_field: ImageField,
    image_rotation: float = -3,
    card_rotation: float = 2,
    card_color: str = "#D5C8F4",
) -> str:
    """
    Generate an HTML template for a social media card with specified parameters.
    """
    logo_url = os.path.join(
        settings.BASE_DIR,
        "mediafiles",
        "brand",
        "witz-des-tages-logo-light-full-transparent.png",
    )

    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    html, body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 0;
                        padding: 0;
                        background-color: #f0f0f0;
                        font-family: Inter;
                        width: 1080px;
                        height: 1080px;
                        overflow: hidden;
                    }}

                    .container {{
                        width: 400px;
                        padding: 20px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        transform: scale(2.5);
                        transform-origin: center center;
                        margin-top: -50px;
                    }}

                    .logo-container {{
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-bottom: 1px;
                        width: fit-content;
                        height: auto;
                    }}

                    .logo {{
                        display: block;
                        width: 100px;
                        height: auto;
                        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
                        margin-bottom: 15px;
                    }}

                    .main-image-container {{
                        width: 100%;
                        position: relative;
                    }}

                    .main-image {{
                        width: 280px;
                        height: 280px;
                        border-radius: 20px;
                        transform: rotate({image_rotation}deg);
                        object-fit: cover;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    }}

                    .text-card {{
                        background: {card_color};
                        padding: 10px;
                        border-radius: 15px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        transform: rotate({card_rotation}deg);
                        width: 90%;
                        margin-top: -45px;
                        position: relative;
                        z-index: 2;
                    }}

                    .text-content {{
                        font-family: Inter;
                        font-size: larger;
                        font-weight: bold;
                        color: #333;
                        line-height: 1.4;
                        margin: 0;
                    }}
                </style>
            </head>
                <body>
                    <div class="container">
                        <div class="logo-container">
                            <img class="logo" src="data:image/jpeg;base64,{get_base64_image_from_url(logo_url)}" alt="Logo">
                        </div>
                        
                        <img class="main-image" src="data:image/jpeg;base64,{get_base64_image_from_imagefield(image_field)}" alt="Main content image">
                        
                        <div class="text-card">
                            <p class="text-content">
                                {joke}
                            </p>
                        </div>
                    </div>
                </body>
        </html>
    """

    return template
