import requests
import os  

class StatusMapping:
    def __init__(self, list_id, status):
        self.list_id = list_id
        self.status = status

class Connection():    
    def __init__(self):
        self.url = 'https://api.trello.com/1/' 
        self.key = os.environ['TRELLO_API_KEY']
        self.token = os.environ['TRELLO_API_SECRET']
        self.header = "application/json"

        self.headers = {
            "Accept": self.header
        }

        self.query = {
            'key' : self.key,
            'token': self.token
        }

class TrelloClient(Connection):
    def get_AllBoardList(self):
        response = requests.get(
            self.url + 'members/me/boards/all',
            headers=self.headers,
            params=self.query
        )
        return response
        
    def get_BoardLists(self, id):
        response = requests.get(
            f"{self.url}boards/{id}/lists",
            headers=self.headers,
            params=self.query
        )
        return response
    
    def get_ListCards(self, id):
        response = requests.get(
            self.url + 'lists/' + id + '/cards',
            headers=self.headers,
            params=self.query
        )
        return response
    
    def get_Card(self, id):
        response = requests.get(
            self.url + 'cards/' + id,
            headers=self.headers,
            params=self.query
        )
        return response  

    def create_Card(self, id, name, desc, due):
        query = self.query
        query['idList'] = id
        query['name'] = name
        query['desc'] = desc
        query['due'] = due 

        response = requests.request(
            "POST",
            self.url + 'cards',
            headers=self.headers,
            params=query
        )
        return response   

    def update_Card(self, id, listId, name, desc, due):
        query = self.query
        query['idList'] = listId
        query['name'] = name
        query['desc'] = desc
        query['due'] = due

        response = requests.request(
            "PUT",
            self.url + 'cards/' + id,
            headers=self.headers,
            params=query
        )
        return response 

    def delete_Card(self, id):
        response = requests.request(
            "DELETE",
            self.url + 'cards/' + id,
            headers=self.headers,
            params=self.query
        )
        return response 
        