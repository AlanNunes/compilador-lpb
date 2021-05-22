class Token:
    def __init__(self, id, val, pos):
        # Identificador do token
        self._id = id
        # Valor que o token armazena
        self._val = val
        # Local onde o token está localizado no código-fonte
        self._pos = pos