from todo_app.data.ResponseFilter import ResponseFilter
from flask import session
from operator import attrgetter

sort_order_key = 'sort_order'
sort_descending = 'is_descending'

is_default_sort_order_descending = False
default_sort_order_key = ResponseFilter.title
default_sort_order = {sort_order_key: default_sort_order_key,
                      sort_descending: is_default_sort_order_descending}


def get_current_sort_order():
    return session.get(sort_order_key, default_sort_order)


def set_current_sort_order(sortby):
    current_sort_order = get_current_sort_order()
    if current_sort_order[sort_order_key] == sortby:
        current_sort_order[sort_descending] = not current_sort_order[sort_descending]
    else:
        current_sort_order[sort_descending] = is_default_sort_order_descending

    current_sort_order[sort_order_key] = sortby
    session[sort_order_key] = current_sort_order
    return get_current_sort_order()


def sort(items):
    current_sort_order = get_current_sort_order()
    items.sort(key=attrgetter(
        current_sort_order[sort_order_key]), reverse=current_sort_order[sort_descending])
    return items
