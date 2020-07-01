def key_in_dict_not_empty(key, dictionary):
    """
    """
    if key in dictionary:
        return is_not_empty(dictionary[key])
    return False


def is_empty(value):
    """
    """
    if value is None:
        return True

    return value in ['', [], {}]

def is_not_empty(value):
    return not is_empty(value)