from componentes_parser.instrucao import Instrucao
from typing import List
from componentes_parser.no import No
from componentes_parser.repita import Repita

# repita até <exprArit> então <instrução> fimrepita
class RepitaAte(Repita):
    def __init__(self, expr: No, instrucoes: List[Instrucao]):
        self._expr = expr
        self._instrucoes = instrucoes

    def retornaExpr(self) -> No:
        return self._expr

    def retornaInstrucoes(self) -> List[Instrucao]:
        return self._instrucoes