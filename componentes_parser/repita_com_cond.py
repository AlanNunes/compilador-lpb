from typing import List
import componentes_lexer.tipos_tokens as tipos_tokens
from componentes_parser.no import No
from componentes_parser.repita import Repita
from componentes_parser.instrucao import Instrucao

# repita <declVar>; <cond>; <atribVar> então <instrução> fimrepita |
class RepitaComCond(Repita):
    def __init__(self, decl_var:No, cond: No, atrib_var: No,instrucoes: List[Instrucao]):
        self._decl_var = decl_var
        self._cond = cond
        self._atrib_var = atrib_var
        self._instrucoes = instrucoes

    def retornaDeclVar(self) -> No:
        return self._decl_var
    
    def retornaCond(self) -> No:
        return self._cond

    def retornaAtrVar(self) -> No:
        return self._atrib_var

    def retornaInstrucoes(self) -> List[Instrucao]:
        return self._instrucoes