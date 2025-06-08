import pandas as pd
from sklearn import model_selection

from ..config import Config

CAMPOS = ['tipo', 'conteúdo']
ALVO = 'abertura'


def get_dados() -> pd.DataFrame:
    """
    Leitura dos dados e devoluta somente dos campos de interesse
    """
    df = pd.read_csv('inputs/concursos.csv')[['tipo', 'conteúdo', 'abertura']]

    return df[df['tipo'].isin(Config.TIPOS_POSSÍVEIS)]


def categorizar_dados(df: pd.DataFrame):
    return model_selection.train_test_split(
        df[CAMPOS],
        df[ALVO],
        test_size=Config.TAMANHO_TESTE,
        random_state=Config.SEMENTE_ALEATÓRIA,
        stratify=df[ALVO],
    )
