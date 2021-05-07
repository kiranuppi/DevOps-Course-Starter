def search_list(list, key, value):
    found_item = next((item for item in list if item[key] == value), None)
    return found_item
