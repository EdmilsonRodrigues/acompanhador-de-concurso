import os
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('.env')


class Config:
    DB_URL = os.getenv('DATABASE_URL', None)
    DATA = date.fromisoformat(
        os.getenv('DATA', (date.today() - timedelta(days=1)).isoformat())
    )
    CAMINHO_CATEGORIAS = Path('arquivos', 'categorias.json')
