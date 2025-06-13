class Config:
    MODELO_BASE = 'pt_core_news_sm'
    TIPOS_POSSÍVEIS = {
        'Edital',
        'Edital de Processo Seletivo',
        'Edital de Concurso Público',
    }
    COLUNAS_INTERESSE = [
        'tipo',
        'conteúdo',
        'abertura',
    ]
    SEMENTE_ALEATÓRIA = 42
    TAMANHO_TESTE = 0.2
