import json
from pathlib import Path

import spacy

from .config import Config

nlp = spacy.load(Config.MODELO_BASE)

cont = json.loads(
    Path('modelo_estado', 'inputs', 'conteudos_2025-05-15.json').read_text(
        'utf-8'
    )
)

for document in cont['concurso']:
    doc = nlp(document['conteúdo'])

    for ent in doc.ents:
        print(ent.text, ent.label_)

    print(f'{document['tipo']=}')
    print('\n')
