import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()



API_KEY = os.environ.get('API_KEY')
API_VALUE = os.environ.get('API_TOKEN')
BOARD_ID='602594185d55a18c4ea20b22'
BASE_URL='https://api.trello.com/1'
BOARD_PATH = '/boards/'

LISTS_FROM_BOARD_PATH = BOARD_PATH+BOARD_ID+'/'+'lists'
CARDS_FROM_LIST = 'lists/'


def get_lists_from_board():
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': API_KEY,
        'token': API_VALUE
    }

    response = requests.request(
        "GET",
        BASE_URL+LISTS_FROM_BOARD_PATH,
        headers=headers,
        params=query
    )
    data = response.json()

def get_cards_from_list():
    new_var = get_lists_from_board()
    # url = BASE_URL+CARDS_FROM_LIST+new_var+'/cards'
    url = "https://api.trello.com/1/lists/602594185d55a18c4ea20b23/cards?key=cb605ca676872005168aace21b9fbb90&token=2196313085b9d57c0cffee9e5b4e95326e4fa780b8273d8219461ac061f8a23f"
    
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': API_KEY,
        'token': API_VALUE
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )
    
    jsonResponse = response.json()



