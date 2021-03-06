from componentes_parser.no import No
from token_ import Token

class OpBin(No):
    def __init__(self, esq: No, op: Token, dir: No):
        super().__init__(op)
        self._esq = esq
        self._op = op
        self._dir = dir

    def retornaEsq(self) -> No:
        return self._esq

    def retornaDir(self) -> No:
        return self._dir

    def retornaOp(self) -> Token:
        return self._op