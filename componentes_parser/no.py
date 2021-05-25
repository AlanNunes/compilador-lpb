from token_ import Token

class No:
    def __init__(self, token: Token):
        self._token = token
        self._val = token.retornaValor()

    def retornaToken(self) -> Token:
        return self._token

    def retornaValor(self):
        return self._val