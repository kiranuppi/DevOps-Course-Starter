class User:
    def __init__(self, item):
        self.id = str(item['_id'])
        self.username = item['username']
        self.role = item['role']
