from componentes_lexer.posicao import Posicao
import componentes_lexer


class Token:
    def __init__(self, tipo: componentes_lexer, pos: Posicao, val = None):
        # Identificador do token
        self._tipo = tipo
        # Valor que o token armazena
        self._val = val
        # Local onde o token está localizado no código-fonte
        self._pos = pos

    def __str__(self) -> str:
        return f"(tipo: {self._tipo}, valor: {self._val}, posição: {self._pos})"