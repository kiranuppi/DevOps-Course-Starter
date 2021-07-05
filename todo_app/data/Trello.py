import uuid
from todo_app.TrelloItem import TrelloItem
from todo_app.data.ResponseFilter import ResponseFilter
from todo_app.ListUtils import search_list, to_utc_datetime
import requests
import os

from todo_app.data.Status import Status
from todo_app.data.sort_manager import set_current_sort_order, get_current_sort_order


class trello:
    base_url = 'https://api.trello.com/1/'

    @classmethod
    def init(cls):
        cls.todo_id = None
        cls.doing_id = None
        cls.done_id = None
        cls.lists_from_board = None

        cls.api_key = os.environ.get('API_KEY')
        cls.api_token = os.environ.get('API_TOKEN')
        cls.trello_board_id = os.environ.get('BOARD_ID')

        cls.todo_name = 'To Do'
        cls.in_progress = 'Doing'
        cls.done = 'Done'

        cls.headers = {'key': cls.api_key, 'token': cls.api_token}
        cls.fields_from_cards = {
            'fields': f'{ResponseFilter.name},{ResponseFilter.id_list},{ResponseFilter.last_activity_date}'}

        cls.get_cards_header = cls.headers | cls.fields_from_cards
        cls.get_all_cards_url = f'{cls.base_url}boards/{cls.trello_board_id}/cards'
        cls.fields_from_list = {ResponseFilter.fields: f'{ResponseFilter.name},idBoard'}
        cls.get_lists_headers = cls.headers | cls.fields_from_list
        cls.get_lists_url = f'{cls.base_url}boards/{cls.trello_board_id}/lists'
        cls.cards_url = f'{cls.base_url}cards'
        cls.boards_url = f'{cls.base_url}{ResponseFilter.boards}'
        cls.lists_from_board = None

    @classmethod
    def get_lists(cls):
        if cls.lists_from_board is None:
            cls.lists = requests.get(
                cls.get_lists_url, params=cls.get_cards_header).json()

        return cls.lists

    @classmethod
    def get_id_by_list_name(cls, list_name):
        lists = cls.get_lists()
        return next((item for item in lists if item[ResponseFilter.name] == list_name), None)[ResponseFilter.id]

    @classmethod
    def get_todo_list_id(cls):
        if cls.todo_id is None:
            cls.todo_id = cls.get_id_by_list_name(Status.TODO.value)

        return cls.todo_id

    @classmethod
    def get_doing_list_id(cls):
        if cls.doing_id is None:
            cls.doing_id = cls.get_id_by_list_name(Status.DOING.value)

        return cls.doing_id

    @classmethod
    def get_done_list_id(cls):
        if cls.done_id is None:
            cls.done_id = cls.get_id_by_list_name(Status.DONE.value)

        return cls.done_id

    @staticmethod
    def get_list_items():
        cards = requests.get(
            trello.get_all_cards_url, params=trello.get_cards_header).json()
        lists = trello.get_lists()
        items = []
        for card in cards:
            status = search_list(lists, 'id', card['idList'])['name']
            items.append(TrelloItem(card['id'], card['name'], status, to_utc_datetime(card['dateLastActivity'])))
        return items

    @classmethod
    def add_new_item(cls, item_name):
        list_todo_id = trello.get_todo_list_id()

        payload = {
            ResponseFilter.id_list: list_todo_id,
            ResponseFilter.name: item_name
        }

        new_card_response = requests.post(
            cls.cards_url, params=cls.headers, json=payload).json()

        return new_card_response

    @classmethod
    def move_item(cls, item_id, list_id):
        url = f'{trello.cards_url}/{item_id}'

        payload = {
            ResponseFilter.id_list: list_id
        }
        response = requests.put(
            url=url, params=trello.headers, json=payload).json()
        return response

    @classmethod
    def update_to_inprogress(cls, item_id):
        list_id = trello.get_doing_list_id()
        response = trello.move_item(item_id, list_id)
        return response

    @classmethod
    def update_to_done(cls, item_id):
        list_id = trello.get_done_list_id()
        response = trello.move_item(item_id, list_id)
        return response

    @staticmethod
    def create_board(board_name):
        params = trello.headers | {ResponseFilter.name: board_name}
        print(params)
        print(trello.boards_url)
        response = requests.post(
            url=trello.boards_url, params=params).json()
        return response

    @staticmethod
    def create_temp_board_set_env():
        response = trello.create_board(uuid.uuid4().hex)
        os.environ['BOARD_ID'] = response[ResponseFilter.id]
        return response[ResponseFilter.id]

    @staticmethod
    def delete_board(board_id):
        url = f'{trello.boards_url}/{board_id}'
        response = requests.delete(
            url=url, params=trello.headers)
        return response

    @staticmethod
    def delete_borad_current(board_id):
        return trello.delete_board(board_id)

    @staticmethod
    def get_current_sort_order():
        return get_current_sort_order()

    @staticmethod
    def set_current_sort_order(sortby):
        set_current_sort_order(sortby)
