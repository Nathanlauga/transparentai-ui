import pandas as pd


def get_file_extension(fpath):
    """Returns the extension of a given file
    Parameters
    ----------
    fpath: str
        Path of a file
    Returns
    -------
    str:
        extension of the given file
        the text after the last dot
    """
    return str(fpath).split('.')[-1]


def read_dataset_file(path, nrows=None):
    """
    """
    ext = get_file_extension(path)

    if ext == 'csv':
        return pd.read_csv(path, sep=None, engine='python', nrows=nrows)
    elif ext.startswith('xls'):
        return pd.read_excel(path, nrows=nrows)

    return None
