import pytest

from todo_app.app import create_app
from todo_app.data.Trello import trello
from todo_app.data.ResponseFilter import ResponseFilter
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch, Mock
import json
import os


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


@patch('requests.get')
def test_index_page_mocked(mock_get_requests, client):
    mock_get_requests.side_effect = get_lists_mock
    response = client.get('/')
    assert response.status_code == 200
    assert b'Finished Module 3 test' in response.data
    assert b'Added through Test' in response.data
    assert b'New Todo item through Test' in response.data


@patch('requests.post')
def test_create_board(mock_post_requests):
    mock_post_requests.side_effect = create_board_mock
    board_name = 'A New Test Board'
    new_board = trello.create_board(board_name)
    assert new_board[ResponseFilter.id] == '6059ec106aec31192a803aa6'
    assert new_board[ResponseFilter.name] == board_name


def create_board_mock(url, params):
    if url == trello.boards_url:
        return None
    mock_file = 'new_board'
    response = Mock()
    with open(f'{os.getcwd()}/tests/data/{mock_file}.json') as json_file:
        new_board = json.load(json_file)
        new_board[ResponseFilter.name] = params[ResponseFilter.name]
        response.json.return_value = new_board
    return response


def get_lists_mock(url, params):
    mock_file = None

    if url == trello.get_lists_url:
        mock_file = ResponseFilter.lists
    elif url == trello.get_all_cards_url:
        mock_file = ResponseFilter.cards
    else:
        return None

    response = Mock()
    with open(f'{os.getcwd()}/tests/data/{mock_file}.json') as json_file:
        response.json.return_value = json.load(json_file)
    return response



