from token_ import Token
from componentes_parser.no import No
from componentes_parser.op_bin import OpBin
from componentes_parser.instrucao import Instrucao

class Se(No):
    def __init__(self, cond: No, corpo: Instrucao, senaose: Instrucao=None, senao: Instrucao=None):
        self._cond = cond
        self._corpo = corpo
        self._senaose = senaose
        self._senao = senao

    def retornaCond(self):
        return self._cond

    def retornaCorpo(self):
        return self._corpo

    def retornaSenaoSe(self):
        return self._senaose

    def retornaSenao(self):
        return self._senao