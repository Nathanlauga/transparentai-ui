from transparentai.models import classification
from transparentai.models import regression

from ....utils.db import update_in_db, select_from_db
from ....models import Dataset
from ....models.modules import ModulePerformance


def compute_performance_metrics(df, dataset, metrics=None):
    """
    """
    module = select_from_db(ModulePerformance, 'dataset_id', dataset.id)
    update_in_db(module, {'status': 'loading'})

    try:
        y_true = df[dataset.target]
        y_pred = df[dataset.score]

        if 'classification' in dataset.model_type:
            eval_fn = classification.compute_metrics

            if metrics is None:
                metrics = ['accuracy', 'confusion_matrix', 'roc_auc']
                if 'binary' in dataset.model_type:
                    metrics += ['precision', 'recall', 'f1']
                else:
                    metrics += ['precision_micro', 'recall_micro', 'f1_micro']

        elif dataset.model_type == 'regression':
            eval_fn = regression.compute_metrics

            if metrics is None:
                metrics = ['MAE', 'mean_squared_error',
                           'root_mean_squared_error', 'r2']

        results = eval_fn(y_true, y_pred, metrics)

        data = {'status': 'loaded', 'results': results}
        res = update_in_db(module, data)

        if res != 'updated':
            update_in_db(module, {'status': 'failed'})

    except:
        update_in_db(module, {'status': 'failed'})
