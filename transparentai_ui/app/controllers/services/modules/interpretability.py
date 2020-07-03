from ....utils.db import update_in_db, select_from_db
from ....models.modules import ModuleInterpretability


def compute_global_influence(model, explainer, df):
    """
    """
    module = select_from_db(ModuleInterpretability, 'model_id', model.id)
    update_in_db(module, {'status': 'loading'})

    try:
        var_influence = explainer.explain_global_influence(df)

        data = {'status': 'loaded', 'variable_influence': var_influence}
        res = update_in_db(module, data)

        if res != 'updated':
            update_in_db(module, {'status': 'failed'})

    except Exception as exception:
        print(exception)
        update_in_db(module, {'status': 'failed'})
