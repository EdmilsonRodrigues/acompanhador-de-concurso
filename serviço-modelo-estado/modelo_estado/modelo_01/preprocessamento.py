import re

import pandas as pd
import spacy
from feature_engine import encoding
from sklearn import feature_extraction, preprocessing

from ..config import Config


def get_filtro():
    def filtrar_por_tipo(df: pd.DataFrame):
        return df[df['tipo'].isin(Config.TIPOS_POSSÍVEIS)]

    return preprocessing.FunctionTransformer(filtrar_por_tipo)


def get_preprocessador_conteúdo(nlp: spacy.Language):
    def preprocessar_texto(df: pd.DataFrame):
        df['conteúdo_limpo'] = df['conteúdo'].apply(
            lambda text: _preprocessar_texto(text, nlp)
        )
        return df

    return preprocessing.FunctionTransformer(preprocessar_texto)


def get_vetorizador_conteúdo():
    return feature_extraction.text.TfidfVectorizer(
        max_features=1000, lowercase=False
    )


def get_codificador_tipo():
    return encoding.OneHotEncoder(variables=['tipo'])


def _preprocessar_texto(text, nlp):
    """
    Preprocessa o texto com o Spacy.
    - Remove os números
    - Lematiza o texto
    - Remove as stop words e pontuações
    """
    text = (
        re.sub(r'\d+', '', text)
        .replace('º', '')
        .replace('°', '')
        .replace('/', ' ')
        .replace('ª', '')
    )
    doc = nlp(text)

    lemmas = (
        lower_lemma
        for token in doc
        if not any((token.is_stop, token.is_punct, token.is_space))
        if (lower_lemma := token.lemma_.lower()) not in {'n', 'i', }
    )

    return ' '.join(lemmas)
