def key_in_dict_not_empty(key, dictionary):
    """
    """
    if key in dictionary:
        return dictionary[key] not in ['', []]
    return False