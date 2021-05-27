from token_ import Token
from componentes_parser.no import No
from componentes_parser.op_bin import OpBin

class Condicional(OpBin):
    def __init__(self, esq: No, op: Token, dir: No):
        super().__init__(esq, op, dir)