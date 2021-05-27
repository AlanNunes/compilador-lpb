from token_ import Token
from componentes_parser.no import No
from componentes_parser.op_bin import OpBin
from componentes_parser.instrucao import Instrucao

class Se(No):
    def __init__(self, cond: No, corpo: Instrucao, senaose=None, senao: Instrucao=None):
        self._cond = cond
        self._corpo = corpo
        self._senaose = senaose
        self._senao = senao