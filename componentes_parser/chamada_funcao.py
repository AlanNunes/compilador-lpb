from typing import List
from componentes_parser.no import No
from token_ import Token

# Representa uma chamada (invoke) de função.
class ChamadaFuncao(No):
    def __init__(self, ident: Token, params: List):
        self._ident = ident
        self._params = params

    def retornaIdentificador(self):
        return self._ident

    def retornaParametros(self):
        return self._params