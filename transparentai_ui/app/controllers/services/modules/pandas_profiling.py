from pandas_profiling import ProfileReport
from os.path import dirname, abspath

from ....utils.db import update_in_db, select_from_db
# from ....models.modules import ModulePandasProfiling

from ....models import Dataset

def get_save_path():
    """
    """
    return dirname(dirname(dirname(dirname(abspath(__file__))))) + \
        '/views/modules/pandas_profiling_reports/'

from .... import db

def generate_pandas_prof_report(df, title, explorative=False, dataset=None):
    """
    """
    try:
        profile = ProfileReport(df, title=title, explorative=explorative)

        output_path = get_save_path()
        output_path = output_path + title + '.html'

        profile.to_file(output_path)
        
        if dataset is not None:
            dataset = select_from_db(Dataset, 'name', dataset.name)

            data = {'status': 'loaded', 'path': output_path}            
            res = update_in_db(dataset.module_pandas_profiling, data)

            if res != 'updated':
                update_in_db(dataset.module_pandas_profiling, {'status': 'failed'})

    except:
        if dataset is not None:
            dataset = select_from_db(Dataset, 'name', dataset.name)
            update_in_db(dataset.module_pandas_profiling, {'status': 'failed'})
