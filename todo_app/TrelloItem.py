class TrelloItem:

    def __init__(self, id, title, status, datetime):
        self.id = id
        self.title = title
        self.status = status
        self.date_last_activity = datetime
