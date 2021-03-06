def combine_lists(main_list, joining_list, join_key):
    for row in main_list:
        join_value = row[join_key]
        joining_row = search_list(joining_list, join_key, join_value)
        row.update(joining_row)
    return main_list


def swap_key_in_list(list, old_key, new_key):
    for row in list:
        if old_key in row:
            row[new_key] = row.pop(old_key)
    return list


def search_list(list, key, value):
    found_item = next((item for item in list if item[key] == value), None)
    return found_item
