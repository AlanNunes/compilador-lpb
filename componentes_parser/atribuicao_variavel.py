from token_ import Token
from componentes_parser.no import No
from componentes_parser.op_bin import OpBin

class AtribuicaoVariavel(OpBin):
    def __init__(self, ident: No, op: Token, val: No):
        super().__init__(ident, op, val)