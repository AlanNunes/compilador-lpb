from typing import List
from componentes_parser.parametro import Parametro
from componentes_parser.no import No
from componentes_parser.instrucao import Instrucao
from token_ import Token

class Funcao(No):
    def __init__(self, ident: Token, params: List[Parametro], instrucao: Instrucao):
        self._ident = ident
        self._params = params
        self._instrucao = instrucao

    def retornaIdentificador(self):
        return self._ident

    def retornaParametros(self):
        return self._params

    def retornaInstrucao(self):
        return self._instrucao