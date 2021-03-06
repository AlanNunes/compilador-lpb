from componentes_parser.no import No
from token_ import Token

# Este Nó representa uma ou mais instruções.
# Em inglês, é conhecido como "statements".
class Instrucao(No):
    def __init__(self, instrucoes=None):
        self._instrucoes = instrucoes
        if instrucoes == None:
            self._instrucoes = []

    def adicionaInstrucao(self, inst):
        self._instrucoes.append(inst)

    def retornaInstrucoes(self):
        return self._instrucoes