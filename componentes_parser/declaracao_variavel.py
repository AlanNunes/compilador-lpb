from componentes_parser.no import No
from token_ import Token

class DeclaracaoVariavel(No):
    def __init__(self, tipo:Token, ident:Token, val:No):
        self._tipo = tipo
        self._ident = ident
        self._val = val

    def retornaTipo(self) -> Token:
        return self._tipo

    def retornaIdentificador(self) -> Token:
        return self._ident

    def retornaValor(self) -> Token:
        return self._val 