import os
import requests
import base64


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
