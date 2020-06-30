
def format_str_strip(form_data, key):
    """
    """
    if key not in form_data:
        return ''

    return form_data[key].strip()


def clean_errors(errors):
    """
    """
    new_errors = dict()
    for k, v in errors.items():
        if v is not None:
            new_errors[k] = v
    return new_errors
