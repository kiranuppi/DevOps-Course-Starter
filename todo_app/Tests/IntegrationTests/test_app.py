from unittest.mock import Mock, patch

import pytest
from flask.cli import load_dotenv
from dotenv import load_dotenv, find_dotenv

from todo_app import app
from todo_app.Tests.mock import TEST_BOARD_ID


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')


def mock_get_lists(url, params):
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = [
            {
                "id": "602594185d55a18c4ea20b23",
                "name": "To Do",
                "closed": false,
                "pos": 16384,
                "softLimit": null,
                "idBoard": "602594185d55a18c4ea20b22",
                "subscribed": false
            },
            {
                "id": "602594185d55a18c4ea20b24",
                "name": "Doing",
                "closed": false,
                "pos": 32768,
                "softLimit": null,
                "idBoard": "602594185d55a18c4ea20b22",
                "subscribed": false
            },
            {
                "id": "602594185d55a18c4ea20b25",
                "name": "Done",
                "closed": false,
                "pos": 49152,
                "softLimit": null,
                "idBoard": "602594185d55a18c4ea20b22",
                "subscribed": false
            }
        ]
        return response
    return None


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client
