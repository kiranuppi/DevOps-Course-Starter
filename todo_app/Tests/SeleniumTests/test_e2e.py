import os
from threading import Thread
import pytest
import requests
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver

import todo_app.app as app

file_path = find_dotenv('.env')
load_dotenv()
api_key = os.environ.get('API_KEY')
api_token = os.environ.get('API_TOKEN')
base_url = 'https://api.trello.com/1'
todo_item = 'TemporaryTrelloBoard'


def create_trello_board():
    # url = "https://api.trello.com/1/boards/"
    url = f'{base_url}/boards'

    query = {
        'key': api_key,
        'token': api_token,
        'name': todo_item
    }

    response = requests.request(
        "POST",
        url,
        params=query
    )

    return response.json()['id']


def delete_trello_board(board_id):
    # url = "https://api.trello.com/1/boards/" + board_id
    url = f'{base_url}/boards/{board_id}'

    query = {
        'key': api_key,
        'token': api_token
    }

    response = requests.request(
        "DELETE",
        url,
        params=query
    )


@pytest.fixture(scope='module')
def app_with_temp_board():

    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_check_app(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'


# def test_create_new_to_do_item(driver, app_with_temp_board):
#     driver.find_element_by_name("title").send_keys(todo_item)
#     driver.find_element_by_name("submit").click()
#     assert todo_item in driver.page_source
#     action = driver.find_element_by_xpath("//table/tbody/tr[contains(string(), " + todo_item + ")]//a")
#     status = driver.find_element_by_xpath("//table/tbody/tr[contains(string(), " + todo_item + ")]//p")
#     assert action == "Move it Doing"
#     assert status == "To Do"
#
#
# def test_move_inprogress_item_to_done(driver, app_with_temp_board):
#     action = driver.find_element_by_xpath("//table/tbody/tr[contains(string(), " + todo_item + ")]//a")
#     action.click()
#     assert action == "Move it to Done"
#     status = driver.find_element_by_xpath("//table/tbody/tr[contains(string(), " + todo_item + ")]//p")
#     assert status == "Doing"
#
#
# def test_move_done_item_to_todo(driver, app_with_temp_board):
#     action = driver.find_element_by_xpath("//table/tbody/tr[contains(string(), " + todo_item + ")]//a")
#     action.click()
#     assert action == "Repeat Task"
#     status = driver.find_element_by_xpath("//table/tbody/tr[contains(string(), " + todo_item + ")]//p")
#     assert status == "Done"
