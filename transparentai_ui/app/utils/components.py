
def get_request_attribute(form_data, key, default=''):
    """
    """
    if key not in form_data:
        return ''
    return form_data[key]


def get_component_args(data, attributes):
    """
    """
    args = dict()

    # Retrieve Attributes from request.form
    for attr in attributes:
        args[attr] = get_request_attribute(data, attr)

    return args


def list_property(attr, unique=False):
    format_list = [str(x).replace('//,', ';')
                   for x in attr.split(';') if str(x) != '']
    if unique:
        return list(set(format_list))
    return format_list


def list_property_setter(attr, value):
    if attr is None:
        attr = ''

    if type(value) == list:
        for v in value:
            v = v.replace(';', '//,')
            attr += ';%s' % str(v)
    else:
        value = value.replace(';', '//,')
        attr += ';%s' % str(value)

    return attr


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
