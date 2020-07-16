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


def drop_dupplicates_values(values):
    seen = set()
    seen_add = seen.add
    return [x for x in values if not (x in seen or seen_add(x))]