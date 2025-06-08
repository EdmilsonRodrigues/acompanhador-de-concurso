from sklearn import model_selection, naive_bayes


def get_grid():
    model = naive_bayes.MultinomialNB()

    params = {
        'alpha': [
            0.021,
            0.022,
            0.023,
            0.024,
            0.025,
            0.026,
            0.027,
            0.028,
            0.029,
            0.030,
        ],
    }

    return model_selection.GridSearchCV(
        model,
        param_grid=params,
        n_jobs=-1,
        scoring='recall',
    )
