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


def read_dataset_file(path, nrows=None, sep=',', encoding='utf_8'):
    """
    """
    ext = get_file_extension(path)

    if ext == 'csv':
        return pd.read_csv(path, sep=sep, encoding=encoding, nrows=nrows)
    elif ext.startswith('xls'):
        return pd.read_excel(path, encoding=encoding, nrows=nrows)

    return None


def get_file_length(fpath):
    """
    """
    with open(fpath, 'r') as file:
        cnt = sum(1 for row in file) - 1
    file.close()

    return cnt