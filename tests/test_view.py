"""Unit tests for view.py"""

from todo_app.models.view import View
from todo_app.models.card import Card
import datetime

sample_data = [
    {"_id":"617c478ba79ad94f59ba815a", "name":"Task1", "due":"2021-10-26T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task1", "status":"To Do"},
    {"_id":"617c478ba79ad94f59ba815b", "name":"Task2", "due":"2021-10-27T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task2", "status":"Doing"},
    {"_id":"617c478ba79ad94f59ba815c", "name":"Task3", "due":"2021-10-28T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task3", "status":"Done"},
    {"_id":"617c478ba79ad94f59ba815d", "name":"Task4", "due":"2021-10-29T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task4", "status":"To Do"},
    {"_id":"617c478ba79ad94f59ba815e", "name":"Task5", "due":"2021-10-26T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task5", "status":"Doing"},
    {"_id":"617c478ba79ad94f59ba815f", "name":"Task6", "due":"2021-10-30T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task6", "status":"Done"},
    {"_id":"617c478ba79ad94f59ba815g", "name":"Task7", "due":"2021-10-25T00:00:00.000+00:00", "dateLastActivity":datetime.datetime.strptime((datetime.datetime.utcnow()).strftime("%Y-%m-%d"), '%Y-%m-%d'), "desc":"Task7", "status":"Done"}
]

cardslist = []
for card in sample_data:
    cardslist.append(Card(card))   
 
def test_viewmodel_empty_filterToDo_only():
    emptyViewModel = View([])
    assert len(emptyViewModel.todo) == 0

def test_viewmodel_filterTodo_only():
    view_model = View(cardslist)
    result = view_model.todo 
    assert len(result) == 2
    assert result[0].status == "To Do"

def test_viewmodel_empty_filterDoing_only():
    emptyViewModel = View([])
    assert len(emptyViewModel.doing) == 0

def test_viewmodel_filterDoing_only():
    view_model = View(cardslist)
    result = view_model.doing
    assert result[0].status == "Doing"
    assert len(result) == 2

def test_viewmodel_empty_filterDone_only():
    emptyViewModel = View([])
    assert len(emptyViewModel.show_all_done_items) == 0

def test_viewmodel_filter_Show_all_done_items():
    view_model = View(cardslist)
    result = view_model.show_all_done_items
    assert result[0].status == "Done"
    assert len(result) == 3

def test_viewmodel_filter_recent_done_items():
    view_model = View(cardslist)
    result = view_model.recent_done_items
    assert result[0].status == "Done"
    assert len(result) == 1

def test_viewmodel_filter_older_done_items():
    view_model = View(cardslist)
    result = view_model.older_done_items
    assert result[0].status == "Done"
    assert len(result) == 2