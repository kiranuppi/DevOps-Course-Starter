
import os
import time
import uuid
from threading import Thread
import pytest
import requests
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver

from todo_app.app import create_app
from todo_app.data.Trello import trello


@pytest.fixture(scope='module')
def app_with_temp_board():
    # Use real config instead of the 'test' version
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    trello.init()
    trello.create_temp_board_set_env()

    print(os.environ['BOARD_ID'])
    app = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    print(f'Board Id before deleting is: {trello.trello_board_id}')
    trello.delete_borad_current(trello.trello_board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    time.sleep(6)
    driver.get("http://localhost:5000/")
    driver.implicitly_wait(5)
    assert driver.title == 'To-Do App'

    start_button_text = ".//a[contains(text(), 'Start')]"
    done_button_text = '.btn.btn-outline-secondary.btn-sm'

    # Test creating a new task and check if it exists on the web page
    task_name = 'Add new Task.'
    input_task_title = driver.find_element_by_id("title")

    input_task_title.click()
    input_task_title.clear()
    input_task_title.send_keys(task_name)
    input_task_title.submit()
    time.sleep(10)
    assert task_name in driver.page_source

    # Navigate to the To Do Tab
    tab_todo = driver.find_element_by_id("nav-todo-tab")
    tab_todo.click()
    time.sleep(3)
    # Start the new To Do task
    start_button = driver.find_element_by_xpath(start_button_text)
    start_button.click()
    time.sleep(3)
    assert task_name in driver.page_source

    # Navigate to the Doing Tab
    tab_doing = driver.find_element_by_id("nav-doing-tab")
    tab_doing.click()
    time.sleep(3)
    # Complete the Doing task
    done_button = driver.find_element_by_css_selector(
        done_button_text)
    done_button.click()
    time.sleep(3)
    assert task_name in driver.page_source

