import pytest
from fastapi.testclient import TestClient
from backend.constants import SYSTEM_PROMPT, USER_PROMPT
from backend.server import app
from unittest.mock import patch

# Initialize TestClient with the FastAPI app for testing
client = TestClient(app)


def test_health_check():
    """
    Test the health check endpoint to ensure it's working correctly.
    """
    # Make a GET request to the health check endpoint
    response = client.get("/")
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response JSON matches the expected output
    assert response.json() == {"ping": "pong"}


@pytest.fixture
def mock_chroma_collection():
    """
    Pytest fixture to mock the chroma_collection used in the server.
    """
    # Use patch to mock the chroma_collection object in the backend.server module
    with patch('backend.server.chroma_collection', autospec=True) as mock_chroma_collection:
        yield mock_chroma_collection


@pytest.fixture
def mock_prompt_llm():
    """
    Pytest fixture to mock the prompt_llm function used in the server.
    """
    # Use patch to mock the prompt_llm function in the backend.server module
    with patch('backend.server.prompt_llm') as mock_prompt_llm:
        yield mock_prompt_llm


def test_recommend_anime(mock_chroma_collection, mock_prompt_llm):
    """
    Test the recommend_anime endpoint to ensure it returns the correct recommendation.
    """
    # Mock the query response from chroma_collection
    mock_chroma_collection.query.return_value = {
        "metadatas": [
            [{"summary": "Mock summary 1"}, {"summary": "Mock summary 2"}]
        ]
    }
    # Mock the response from the prompt_llm function
    mock_prompt_llm.return_value = "Mocked LLM response"

    # Make a POST request to the recommend_anime endpoint with a test prompt
    response = client.post("/recommend-anime", json={"prompt": "test prompt"})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response JSON matches the expected recommendation
    assert response.json() == {"recommendation": "Mocked LLM response"}

    # Assert that the chroma_collection.query method was called once with the correct arguments
    mock_chroma_collection.query.assert_called_once()
    assert mock_chroma_collection.query.call_args[1]['query_texts'] == [
        "test prompt"]

    # Assert that the prompt_llm function was called once with the correct arguments
    templated_user_prompt = USER_PROMPT.format(
        system_prompt=SYSTEM_PROMPT,
        context="Mock summary 1\n\nMock summary 2",
        question="test prompt"
    )
    mock_prompt_llm.assert_called_once_with(templated_user_prompt)


def test_recommend_anime_exception(mock_chroma_collection):
    """
    Test the recommend_anime endpoint to ensure it handles exceptions correctly.
    """
    # Mock the chroma_collection.query method to raise an exception
    mock_chroma_collection.query.side_effect = Exception("Test exception")

    # Make a POST request to the recommend_anime endpoint with a test prompt
    response = client.post("/recommend-anime", json={"prompt": "test prompt"})

    # Assert that the response status code is 500 (Internal Server Error)
    assert response.status_code == 500
    # Assert that the response JSON contains the exception detail
    assert response.json() == {"detail": "Test exception"}
