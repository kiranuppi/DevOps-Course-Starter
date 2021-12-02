import datetime


class View:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo(self):
        _todo_ls = [item for item in self._items if item.status == "To Do"]
        return _todo_ls

    @property
    def doing(self):
        _doing_ls = [item for item in self._items if item.status == "Doing"]
        return _doing_ls

    @property
    def recent_done_items(self):
        _done_ls = [item for item in self._items if item.dateLastActivity == datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d') and item.status == "Done"]
        return _done_ls
    
    @property
    def show_all_done_items(self):
        _done_ls = [item for item in self._items if item.status == "Done"]
        if len(_done_ls) < 5:
            return _done_ls
        else:
            _done_ls = [item for item in self._items if item.dateLastActivity == datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d') and item.status == "Done"]
            return _done_ls

    @property
    def older_done_items(self):
        _done_ls = [item for item in self._items if item.dateLastActivity != datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d') and item.status == "Done"]
        return _done_ls

    @property
    def allusers(self):
        _users_ls = [item for item in self._items]
        return _users_ls