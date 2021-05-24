class Posicao:
    _linha = 0
    _coluna = 0
    _arquivo = ''
    def __init__(self, linha: int, coluna: int, arquivo: str = ''):
        self._linha = linha
        self._coluna = coluna
        self._arquivo = arquivo

    def __str__(self) -> str:
        return f"(coluna: {self._coluna}, linha: {self._linha}, fonte: {self._arquivo})"

    def retornaLinha(self) -> int:
        return self._linha
        
    def retornaColuna(self) -> int:
        return self._coluna