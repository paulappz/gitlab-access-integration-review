import pytest
from unittest.mock import Mock
from api.gitlab_client import GitLabAPIClient

@pytest.fixture
def mock_client(mocker):
    # Mock environment variables
    mocker.patch("os.getenv", side_effect=lambda x: "mock_value" if x == "PRIVATE_TOKEN" else "https://gitlab.example.com")
    client = GitLabAPIClient()
    
    # Mock requests.get
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "name": "Test User"}]
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)
    
    return client

def test_get_external_users(mock_client):
    users = mock_client.get_external_users()
    assert len(users) == 1
    assert users[0]["name"] == "Test User"

def test_get_project_tokens(mock_client):
    tokens = mock_client.get_project_tokens(123)
    assert len(tokens) == 1

def test_error_handling(mocker, mock_client):
    # Simulate HTTP error
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mocker.patch("requests.get", return_value=mock_response)
    
    with pytest.raises(requests.exceptions.HTTPError):
        mock_client.get_external_users()