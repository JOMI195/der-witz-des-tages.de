import os
from openai import OpenAI


def generateJokePicturePrompt(promptContent: str) -> str:
    MODEL = "gpt-4o"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = 'Give a visual representation in two detailed sentences of the following german joke: "{promptContent}". Start your answer with: the representation shows . Also do not include written text, names or speech bubbles in the answer.'.format(
        promptContent=promptContent
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            # {
            #     "role": "system",
            #     "content": "You are a helpful assistant. Help me with my math homework!",
            # },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        # temperature=1.3,
        # max_tokens=256,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0,
    )

    # if not response or "choices" not in response:
    #     raise ValueError("Invalid response from OpenAI API")

    generated_text = response.choices[0].message.content

    return generated_text
