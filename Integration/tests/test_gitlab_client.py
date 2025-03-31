import pytest
import requests
from unittest.mock import Mock, patch
from api.gitlab_client import GitLabAPIClient
from datetime import datetime, timedelta


@pytest.fixture(autouse=True)
def no_sleep():
    with patch("time.sleep", return_value=None):
        yield

@pytest.fixture
def mock_client(mocker):
    mocker.patch("os.getenv", side_effect=lambda k, d=None: {
        "GITLAB_URL": "https://gitlab.example.com",
        "PRIVATE_TOKEN": "mock_value"
    }.get(k, d))
    return GitLabAPIClient()

def mock_responses(*data_pages):
    """Generates mocked responses for paginated endpoints."""
    return [
        Mock(**{
            "json.return_value": page_data,
            "raise_for_status.return_value": None
        }) for page_data in data_pages
    ]

def test_get_external_users(mock_client, mocker):
    # Mock a user with external=True
    mocker.patch("requests.get", side_effect=mock_responses(
        [{"id": 1, "name": "Test User", "external": True}],
        []
    ))
    
    users = mock_client.get_external_users()
    assert len(users) == 1
    assert users[0]["name"] == "Test User"


def test_get_project_tokens(mock_client, mocker):
    # Page 1: 1 token, Page 2: empty
    mocker.patch("requests.get", side_effect=mock_responses(
        [{"id": 1, "name": "test-token", "scopes": ["api"]}],
        []
    ))
    
    tokens = mock_client.get_project_tokens(2)
    assert len(tokens) == 1
    assert tokens[0]["name"] == "test-token"

def test_get_pipelines(mock_client, mocker):
    # Page 1: 1 pipeline, Page 2: empty
    mocker.patch("requests.get", side_effect=mock_responses(
        [{"id": 1, "status": "success", "ref": "main"}],
        []
    ))
    
    pipelines = mock_client.get_pipelines(2)
    assert len(pipelines) == 1
    assert pipelines[0]["status"] == "success"

def test_get_webhooks(mock_client, mocker):
    # Page 1: 1 webhook, Page 2: empty
    mocker.patch("requests.get", side_effect=mock_responses(
        [{"id": 1, "url": "https://webhook.site", "push_events": True}],
        []
    ))
    
    hooks = mock_client.get_webhooks(2)
    assert len(hooks) == 1
    assert hooks[0]["url"] == "https://webhook.site"

def test_get_instance_audit_logs(mock_client, mocker):
    # Page 1: 1 audit log, Page 2: empty
    mocker.patch("requests.get", side_effect=mock_responses(
        [{"id": 1, "action": "logged_in", "author_id": 1}],
        []
    ))
    
    logs = mock_client.get_instance_audit_logs()
    assert len(logs) == 1
    assert logs[0]["action"] == "logged_in"

def test_error_handling(mock_client, mocker):
    error_response = Mock()
    error_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mocker.patch("requests.get", return_value=error_response)
    
    # Expect no exception, but result should be empty
    result = mock_client._paginated_get("projects/2/access_tokens")
    assert result == []

def test_check_token_expiry_filters(mock_client, mocker):
    today = datetime.now()
    token_list = [
        {
            "id": 1,
            "name": "test-token",
            "created_at": (today - timedelta(days=40)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "expires_at": (today + timedelta(days=10)).strftime("%Y-%m-%d"),
        },
        {
            "id": 2,
            "name": "another-token",
            "created_at": (today - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "expires_at": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
        },
    ]

    mocker.patch("requests.get", side_effect=mock_responses(token_list, []))
    
    results = mock_client.check_token_expiry(
        project_id=2,
        days_threshold=15,
        token_name="test",
        created_before=(today - timedelta(days=20)).strftime("%Y-%m-%d"),
        created_after=(today - timedelta(days=60)).strftime("%Y-%m-%d")
    )
    
    assert len(results) == 1
    assert results[0]["name"] == "test-token"
