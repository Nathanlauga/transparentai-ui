from flask_babel import _


def get_errors():
    """
    """
    errors_dict = {
        'ReadCsvError': _('Inputed csv file not valid.'),
        'ReadDatasetFromFileError': _('File not valid'),
        'AddInDB': _('Failed to add object in database.'),
        'UpdateInDB': _('Failed to Update object in database.'),
        'DeleteInDB': _('Failed to delete object in database.'),
        'ModelNameNotSet': _('The name of the model is not set'),
        'ModelNameAlreadyUsed': _('The model name is already used.'),
        'ModelPathNoType': _('You need to specify a model type with the path'),
        'ModelPathNotExists': _('The model path is not pointing to a file.'),
        'ModelPathCantOpen': _('Impossible to open the model file.'),
        'ModelFileTypeNotValid': _('Model file type is not a valid one, please use one of the following : pickle or joblib'),
        'DatasetNameNotSet': _('The name of the dataset is not set'),
        'DatasetNameAlreadyUsed': _('The model dataset is already used.'),
        'DatasetPathNotExists': _('The dataset path is not pointing to a file.'),
        'DatasetPathExtension': _('The dataset extension is not valid.'),
        'DatasetPathCantOpen': _('Impossible to open the dataset file. Check that you can open your file with an other application.'),
        'DatasetColumnNotFound': _(' column not found in the data.'),
        'DatasetModelTypeNotValid': _('The dataset model type is not valid, please use one of the following : binary-classification, multiclass-classification or regression')
    }

    return errors_dict
