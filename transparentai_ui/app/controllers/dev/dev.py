from flask import render_template, request
from flask import current_app as app
from flask_babel import _

import pandas as pd
from ...utils.errors import Error

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
    ext = get_file_extension(fpath)

    if ext == 'csv':
        try:
            data = pd.read_csv(fpath, sep=None)
        except:
            return Error.ReadCsvError


    else:
        return "Validation not"

    return data


def load_csv():

    if 'dataset-path' in request.form:
        data_path = request.form['dataset-path']
        dataset = retrieve_dataset_from_file(data_path)

        if type(dataset) == Error:
            # file not valid
            return render_template('dev/load_csv.html', error=dataset)

        dataset = dataset.head(5).to_html(header="true", table_id="dataset")

        return render_template('dev/load_csv.html', dataset=dataset)
    return render_template('dev/load_csv.html')
