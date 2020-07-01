from pandas_profiling import ProfileReport
from os.path import dirname, abspath

from ....utils.db import update_in_db, select_from_db

from ....models import Dataset
from ....models.modules import ModulePandasProfiling


def get_save_path():
    """
    """
    return dirname(dirname(dirname(dirname(abspath(__file__))))) + \
        '/views/modules/pandas_profiling_reports/'


def generate_pandas_prof_report(df, title, explorative=False, dataset=None):
    """
    """
    if dataset is not None:
        module = select_from_db(ModulePandasProfiling, 'dataset_id', dataset.id)
        update_in_db(module, {'status': 'loading'})

    try:
        profile = ProfileReport(df, title=title, explorative=explorative)

        output_path = get_save_path()
        output_path = output_path + title + '.html'

        profile.to_file(output_path)

        if dataset is not None:
            data = {'status': 'loaded', 'path': output_path}
            res = update_in_db(module, data)

            if res != 'updated':
                update_in_db(module, {'status': 'failed'})

    except:
        if dataset is not None:
            update_in_db(module, {'status': 'failed'})
