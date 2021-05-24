from componentes_lexer.posicao import Posicao
import componentes_lexer

# O Token representa um símbolo abstrato de cada elemento
#  que compõe o programa. Ele representa as palavras-chaves
#  valores numéricos, valores de texto, instruções, operações
#  binárias e etc... 
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