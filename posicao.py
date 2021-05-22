class Posicao:
    _linha = 0
    _coluna = 0
    def __init__(self, linha, coluna):
        _linha = linha
        _coluna = coluna

    def retornaLinha(self):
        return self._linha
        
    def retornaColuna(self):
        return self._coluna