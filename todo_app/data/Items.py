from todo_app.data.ResponseFilter import ResponseFilter
from todo_app.Trello_Item import Trello_Item
from todo_app.data.Trello import trello


class Items:

    @staticmethod
    def get_all_items():
        trello_items = trello.get_list_items()
        items = []
        for trello_item in trello_items:
            items.append(
                Trello_Item(trello_item[ResponseFilter.id], trello_item[ResponseFilter.name],
                            trello_item[ResponseFilter.status]))
        return items

    @staticmethod
    def add_new_item(item_name):
        return trello.add_new_item(item_name)

    @staticmethod
    def update_item_to_inprogress(item_id):
        return trello.update_to_inprogress(item_id)

    @staticmethod
    def update_item_to_done(item_id):
        return trello.update_to_done(item_id)
