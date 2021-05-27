from componentes_parser.se import Se
from componentes_parser.no import No
from componentes_parser.instrucao import Instrucao

class SenaoSe(Se):
    def __init__(self, cond: No, corpo: Instrucao, senaose: Se=None, senao: Instrucao=None):
        super().__init__(cond, corpo, senaose=senaose, senao=senao)
