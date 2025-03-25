def get_param_grid():
    return {
        'n_estimators': [50, 100],
        'max_depth': [3, 5],
        'learning_rate': [0.01, 0.1],
        'subsample': [0.8, 1.0],
        # 'col-sample_bytree': [0.8, 1.0]
    }
