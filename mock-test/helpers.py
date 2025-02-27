import os
import requests
from dotenv import load_dotenv  # Third-party import

# Load environment variables from .env file
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

def get_chat_response(message: str) -> str:
    """Sends a message to OpenAI's API and returns the response."""
    url = "https://api.openai.com/v1/chat/completions"
    api_key = OPENAI_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]