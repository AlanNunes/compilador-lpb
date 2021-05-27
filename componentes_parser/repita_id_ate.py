from typing import List
from componentes_lexer.tipos_tokens import identificador
from componentes_parser.no import No
from componentes_parser.repita import Repita
from componentes_parser.instrucao import Instrucao

# repita <id> até <exprArit> então <instrução> fimrepita |
class RepitaIdentAte(Repita):
    def __init__(self, ident:identificador, expr: No, instrucoes: List[Instrucao]):
        self._expr = expr
        self._ident = ident
        self._instrucoes = instrucoes

    def retornaIdentificador(self) -> No:
        return self._ident

    def retornaExpr(self) -> No:
        return self._expr

    def retornaInstrucoes(self) -> List[Instrucao]:
        return self._instrucoes