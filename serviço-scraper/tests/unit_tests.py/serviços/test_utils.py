from serviço_scraper.serviços.utils import implementa


def test_implementa():
    def função_com_documentação():
        """
        Documentação da função
        """
        pass

    @implementa(função_com_documentação)
    def função():
        pass

    assert função.__doc__
    assert função.__doc__ == função_com_documentação.__doc__
