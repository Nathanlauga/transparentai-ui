from pandas_profiling import ProfileReport
from os.path import dirname, abspath


def get_save_path():
    """
    """
    return dirname(dirname(dirname(abspath(__file__)))) + '/views/modules/pandas_profiling_reports/'


def generate_pandas_prof_report(df, title, explorative=False):
    """
    """
    profile = ProfileReport(df, title=title, explorative=explorative)

    output_path = get_save_path()
    output_path = output_path + title + '.html'

    profile.to_file(output_path)
