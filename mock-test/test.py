import os
import pytest
from unittest.mock import patch
from helpers import get_chat_response  # Adjust import to match your file structure
from dotenv import load_dotenv  # Third-party import

# Load environment variables from .env file
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

@pytest.fixture
def mock_api_response():
    """Fixture to mock API response."""
    return {
        "choices": [{"message": {"content": "Mocked response"}}]
    }

@patch("requests.post")  # Mock requests.post globally for this test
def test_get_chat_response(mock_post, mock_api_response):
    """Test get_chat_response without hitting the real API."""

    # Mock the API response
    mock_post.return_value.json.return_value = mock_api_response

    # Call the function (it will use the mock)
    response = get_chat_response("Hello!")

    # Assertions
    assert response == "Mocked response"
    mock_post.assert_called_once_with(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello!"}],
            "temperature": 0.5
        }
    )
