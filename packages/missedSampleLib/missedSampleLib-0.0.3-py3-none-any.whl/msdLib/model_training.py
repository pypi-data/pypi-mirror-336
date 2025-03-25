import math

import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from xgboost import XGBClassifier


# noinspection SpellCheckingInspection
def train_model(x_train, y_train, param_grid):
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    xgb = XGBClassifier(
        eval_metric="auc",
        random_state=42,
        missing=np.nan
    )

    grid_search = GridSearchCV(
        estimator=xgb,
        param_grid=param_grid,
        scoring="roc_auc",
        cv=kfold,
        n_jobs=-1,
        verbose=1
    )

    grid_search.fit(x_train, y_train)
    return grid_search


# noinspection SpellCheckingInspection
def evaluate_model(model, x_test):
    y_pred_probs = model.predict_proba(x_test)[:, 1]
    # auc_test = roc_auc_score(y_test, y_pred_probs)
    return y_pred_probs
