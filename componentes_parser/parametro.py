from componentes_parser.declaracao_variavel import DeclaracaoVariavel
from token_ import Token
from componentes_parser.no import No

class Parametro(DeclaracaoVariavel):
    def __init__(self, tipo: Token, ident: Token, val: No):
        super().__init__(tipo, ident, val)