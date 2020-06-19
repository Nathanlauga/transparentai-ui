from flask import render_template, request
from flask import current_app as app
from flask_babel import _

import pandas as pd
from ...utils.errors import get_errors


def dev():
    title = _('Dev page')
    return render_template("dev/index.html", title=title)


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


def retrieve_dataset_from_file(fpath):
    """
    """
    errors_dict = get_errors()
    ext = get_file_extension(fpath)

    if ext == 'csv':
        try:
            data = pd.read_csv(fpath, sep=None, engine='python')
        except:
            return errors_dict['ReadCsvError']

    else:
        return errors_dict['ReadDatasetFromFileError']

    return data


def load_csv():
    title = _('Load dataset')

    if 'dataset-path' in request.form:
        data_path = request.form['dataset-path']
        dataset = retrieve_dataset_from_file(data_path)

        if type(dataset) != pd.DataFrame:
            # file not valid
            return render_template('dev/load_csv.html', error=dataset, title=title)

        dataset = dataset.head(5).to_html(header="true", table_id="dataset")

        return render_template('dev/load_csv.html', dataset=dataset, title=title)
    return render_template('dev/load_csv.html', title=title)
