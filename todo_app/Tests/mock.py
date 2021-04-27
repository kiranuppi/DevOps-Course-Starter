import json
import os
from unittest.mock import Mock

from requests import patch

api_key = os.environ.get('API_KEY')
api_token = os.environ.get('API_TOKEN')
TEST_BOARD_ID = os.environ.get('BOARD_ID')


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')


def mock_get_lists(url, params):
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        with open('example.json', 'r') as myfile:
            data = myfile.read()
            response.json.return_value = json.loads(data)
            return response
    return None
