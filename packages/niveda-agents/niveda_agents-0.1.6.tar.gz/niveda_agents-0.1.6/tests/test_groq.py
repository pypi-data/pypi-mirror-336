import os
import pytest
from unittest.mock import patch, MagicMock
from niveda_agents.ai.groq import GroqClient


@pytest.fixture
@patch.dict(os.environ, {"GROQ_API_KEY": "test_api_key"})
def groq_client():
    """Fixture to initialize GroqClient with a mock API key."""
    return GroqClient()


def test_initialize_groq_client(groq_client):
    """Test GroqClient initialization with API key."""
    assert groq_client.api_key == "test_api_key"


def test_initialize_groq_client_missing_api_key():
    """Test that GroqClient raises an error if API key is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GROQ_API_KEY is not set."):
            GroqClient()


@patch.object(GroqClient, "generate_text", return_value="Mock response")
def test_generate_text(mock_generate, groq_client):
    """Test generate_text method."""
    response = groq_client.generate_text("Test prompt")
    assert response == "Mock response"
    mock_generate.assert_called_once_with("Test prompt")


@patch.object(GroqClient, "generate_text_with_query", return_value="Mock query response")
def test_generate_text_with_query(mock_generate, groq_client):
    """Test generate_text_with_query method."""
    response = groq_client.generate_text_with_query(
        "Test prompt", "Test query")
    assert response == "Mock query response"
    mock_generate.assert_called_once_with("Test prompt", "Test query")


@patch("niveda_agents.ai.groq.GroqClient")
def test_generate_text_error(mock_groq, groq_client):
    """Test generate_text handles API errors correctly."""
    mock_groq.return_value.chat.completions.create.side_effect = Exception(
        "Error code: 401 - {'error': {'message': 'Invalid API Key', 'type': 'invalid_request_error', 'code': 'invalid_api_key'}}"
    )

    response = groq_client.generate_text("Test prompt")

    assert "Error code: 401" in response
    assert "Invalid API Key" in response


@patch("niveda_agents.ai.groq.GroqClient")
def test_generate_text_with_query_error(mock_groq, groq_client):
    """Test generate_text_with_query handles API errors correctly."""
    mock_groq.return_value.chat.completions.create.side_effect = Exception(
        "Error code: 401 - {'error': {'message': 'Invalid API Key', 'type': 'invalid_request_error', 'code': 'invalid_api_key'}}"
    )

    response = groq_client.generate_text_with_query(
        "Test prompt", "Test query")

    assert "Error code: 401" in response
    assert "Invalid API Key" in response
