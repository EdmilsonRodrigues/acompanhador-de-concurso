import pandas as pd
import spacy
from sklearn import compose, pipeline

from .dados import categorizar_dados, get_dados
from .modelo import get_grid
from .preprocessamento import (
    get_codificador_tipo,
    get_filtro,
    get_preprocessador_conteúdo,
    get_vetorizador_conteúdo,
)


def get_pipeline(nlp: spacy.Language):
    pipeline_preprocessamento = pipeline.Pipeline([
        ('filtrar por tipos possíveis', get_filtro()),
        ('preprocessar conteúdo', get_preprocessador_conteúdo(nlp)),
    ])

    transformação_dados = compose.ColumnTransformer(
        transformers=[
            (
                'vetorizador de texto',
                get_vetorizador_conteúdo(),
                'conteúdo_limpo',
            ),
            ('codificador de tipo', get_codificador_tipo(), ['tipo']),
        ],
        remainder='drop',
    )

    return pipeline.Pipeline([
        ('preparar dados', pipeline_preprocessamento),
        ('transformar dados', transformação_dados),
        ('treinar modelo', get_grid()),
    ])


if __name__ == '__main__':
    from sklearn import metrics

    nlp = spacy.load('pt_core_news_sm')
    pipeline = get_pipeline(nlp)

    X, X_test, y, y_test = categorizar_dados(get_dados())

    pipeline.fit(X, y)

    print(f'{pipeline.named_steps['treinar modelo'].best_params_=}')
    print(f'{pipeline.named_steps['treinar modelo'].best_score_=}')

    y_pred = pipeline.predict(X_test)

    print('--- Model Evaluation Results ---')
    print(f'Accuracy: {metrics.accuracy_score(y_test, y_pred):.2f}')
    print('\nConfusion Matrix:\n\tPredicted')
    print(
        'Actual\n',
        pd.DataFrame(
            data=metrics.confusion_matrix(y_test, y_pred),
            index=['False', 'True'],
            columns=['False', 'True'],
        ),
    )
    print('\nClassification Report:')
    print(metrics.classification_report(y_test, y_pred))

    outros_df = pd.read_json('inputs/outros.json')
    print(list(outros_df['tipo'].unique()))


