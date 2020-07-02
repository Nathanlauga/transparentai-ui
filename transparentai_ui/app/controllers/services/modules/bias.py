from transparentai import fairness

from ....utils.db import update_in_db, select_from_db
from ....utils import is_empty

from ....models import Dataset
from ....models.modules import ModuleBias


def compute_bias_metrics(df, dataset):
    """
    """
    module = select_from_db(ModuleBias, 'dataset_id', dataset.id)
    update_in_db(module, {'status': 'loading'})
    

    y_true = df[dataset.target]
    y_pred = df[dataset.score]

    if is_empty(module.privileged_group):
        privileged_group = {}
        for attr in dataset.protected_attr:
            privileged_group[attr] = [df[attr].value_counts().index[0]]
    else:
        privileged_group = module.privileged_group

    results = fairness.model_bias(y_true, y_pred, df, privileged_group)

    data = {'status': 'loaded', 'results': results,
            'privileged_group': privileged_group}

    try:
        res = update_in_db(module, data)

        if res != 'updated':
            update_in_db(module, {'status': 'failed'})

    except:
        update_in_db(module, {'status': 'failed'})
