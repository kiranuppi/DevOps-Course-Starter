from todo_app.data.ResponseFilter import ResponseFilter
from todo_app.ListUtils import swap_key_in_list, combine_lists
import requests
import os


class trello:
    api_key = os.environ.get('API_KEY')
    api_token = os.environ.get('API_TOKEN')
    trello_board_id = os.environ.get('BOARD_ID')

    todo_name = 'To Do'
    in_progress = 'Doing'
    done = 'Done'
    todo_id = None
    in_progress_id = None
    done_id = None

    base_url = 'https://api.trello.com/1/'

    headers = {'key': api_key, 'token': api_token}

    fields_from_cards = {'fields': f'{ResponseFilter.name},{ResponseFilter.id_list}'}

    get_cards_header = headers | fields_from_cards

    get_all_cards_url = f'{base_url}boards/{trello_board_id}/cards'

    fields_from_list = {ResponseFilter.fields: f'{ResponseFilter.name},idBoard'}

    get_lists_headers = headers | fields_from_list

    get_lists_url = f'{base_url}boards/{trello_board_id}/lists'
    cards_url = f'{base_url}cards'

    lists_from_board = None

    @classmethod
    def get_lists(cls):
        if cls.lists_from_board is None:
            lists = requests.get(
                cls.get_lists_url, params=cls.get_cards_header).json()
            lists = swap_key_in_list(
                lists, ResponseFilter.id, ResponseFilter.id_list)
            cls.lists_from_board = swap_key_in_list(
                lists, ResponseFilter.name, ResponseFilter.status)

        return cls.lists_from_board

    @classmethod
    def get_all_list_ids(cls, list_name):
        lists = cls.get_lists()
        return next((item for item in lists if item[ResponseFilter.status] == list_name), None)[ResponseFilter.id_list]

    @classmethod
    def get_todo_list_id(cls):
        if cls.todo_id is None:
            cls.todo_id = cls.get_all_list_ids(cls.todo_name)

        return cls.todo_id

    @classmethod
    def get_doing_list_id(cls):
        if cls.in_progress_id is None:
            cls.in_progress_id = cls.get_all_list_ids(cls.in_progress)

        return cls.in_progress_id

    @classmethod
    def get_done_list_id(cls):
        if cls.done_id is None:
            cls.done_id = cls.get_all_list_ids(cls.done)

        return cls.done_id

    @staticmethod
    def get_list_items():
        cards = requests.get(
            trello.get_all_cards_url, params=trello.get_cards_header).json()
        lists = trello.get_lists()
        items = combine_lists(
            cards, lists, ResponseFilter.id_list)
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

    @staticmethod
    def move_item(item_id, list_id):
        url = f'{trello.cards_url}/{item_id}'

        payload = {
            ResponseFilter.id_list: list_id
        }
        response = requests.put(
            url=url, params=trello.headers, json=payload).json()
        return response

    @staticmethod
    def update_to_inprogress(item_id):
        list_id = trello.get_doing_list_id()
        response = trello.move_item(item_id, list_id)
        return response

    @staticmethod
    def update_to_done(item_id):
        list_id = trello.get_done_list_id()
        response = trello.move_item(item_id, list_id)
        return response
