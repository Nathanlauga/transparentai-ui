from flask_babel import _


def get_errors():
    """
    """
    errors_dict = {
        'ReadCsvError': _('Inputed csv file not valid.'),
        'ReadDatasetFromFileError': _('File not valid')
    }

    return errors_dict