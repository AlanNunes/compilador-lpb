from componentes_parser.no import No
from token_ import Token

class Boleano(No):
    def __init__(self, token: Token):
        super().__init__(token)