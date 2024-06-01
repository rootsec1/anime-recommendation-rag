import requests
import json

# Local
from constants import MODEL_URL, SYSTEM_PROMPT


def prompt_llm(prompt: str):
    response = requests.post(
        url=MODEL_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer no-key"
        },
        data=json.dumps({
            "model": "LLaMA_CPP",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }),
    )
    response = response.json()
    response = response["choices"][0]["message"]["content"]
    return response
