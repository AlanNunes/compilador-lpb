from componentes_parser.erros.erro import Erro
from componentes_lexer.posicao import Posicao

class ErroIdentJaDefinidoNoEscopo(Erro):
    def __init__(self, msg: str, pos: Posicao):
        super().__init__(msg, pos)

    def retornaErro(self) -> str:
        linha = self._pos.retornaLinha()
        coluna = self._pos.retornaColuna()
        return f"[Identificador já definido] {self._msg}. Erro ocorreu na linha {linha}, coluna {coluna}."