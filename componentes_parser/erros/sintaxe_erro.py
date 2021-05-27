from componentes_parser.erros.erro import Erro
from componentes_lexer.posicao import Posicao

class ErroSintaxe(Erro):
    def __init__(self, msg: str, pos: Posicao):
        super().__init__(msg, pos)

    def retornaErro(self) -> str:
        linha = self._pos.retornaLinha()
        coluna = self._pos.retornaColuna()
        return f"[Erro de sintáxe] {self._msg} na linha {linha}, coluna {coluna}."