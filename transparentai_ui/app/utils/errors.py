from flask_babel import _


def get_errors():
    """
    """
    errors_dict = {
        'ReadCsvError': _('Inputed csv file not valid.'),
        'ReadDatasetFromFileError': _('File not valid'),
        'AddInDB': _('Failed to add object in database.'),
        'UpdateInDB': _('Failed to Update object in database.'),
        'DeleteInDB': _('Failed to delete object in database.')
    }

    return errors_dict