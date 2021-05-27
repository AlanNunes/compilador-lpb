from componentes_lexer.posicao import Posicao

class Erro:
    def __init__(self, msg:str, pos:Posicao):
        self._msg = msg
        self._pos = pos

    def retornaErro(self):
        linha = self._pos.retornaLinha()
        coluna = self._pos.retornaColuna()
        return f"{self._msg} na linha {linha}, coluna {coluna}."