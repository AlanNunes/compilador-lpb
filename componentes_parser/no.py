from token_ import Token

class No:
    def __init__(self, token: Token):
        self._token = token
        self._val = token.retornaValor()