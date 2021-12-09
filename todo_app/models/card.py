class Card:
    def __init__(self, item):
        self.id = str(item['_id'])
        self.name = item['name']
        self.desc = item['desc']
        self.due = item['due']                     
        self.status = item['status']   
        self.dateLastActivity = item['dateLastActivity']