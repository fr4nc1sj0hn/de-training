import os
import sys
import logging
import asyncio
import argparse

from typing import Dict, Any, Optional

import httpx
import markdown
from dotenv import load_dotenv  # Third-party import

# Load environment variables from .env file
load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables if settings is not used
OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_KEY = os.getenv("OPENAI_KEY")

async def get_chat_response_async(message: str) -> str:
    """
    Sends a message to OpenAI's API asynchronously and returns the assistant's response.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_KEY}"
    }
    data = {
        "model": "gpt-4o-mini-2024-07-18",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.5
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENAI_URL, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            assistant_reply = markdown.markdown(response_data['choices'][0]['message']['content'])
            return assistant_reply

    except httpx.HTTPStatusError as http_err:
        return f"HTTP error occurred: {http_err}"
    except httpx.RequestError as req_err:
        return f"Request error occurred: {req_err}"
    except KeyError:
        return "Invalid API response structure."

async def get_multiple_responses(prompts):
    """
    Sends multiple prompts concurrently to OpenAI's API and returns a list of responses.
    """
    tasks = [get_chat_response_async(prompt) for prompt in prompts]
    return await asyncio.gather(*tasks)  # Run all tasks concurrently

# Call async function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get multiple responses from OpenAI API.")
    parser.add_argument("prompts", nargs="+", type=str, help="List of prompts to send to OpenAI.")

    args = parser.parse_args()
    
    # Run the async function
    responses = asyncio.run(get_multiple_responses(args.prompts))

    for i, response in enumerate(responses, 1):
        print(f"\nResponse {i}: {response}")
