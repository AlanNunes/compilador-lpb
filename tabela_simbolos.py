import uuid

class TabelaDeSimbolos:
    def __init__(self, escopo:str=None, pai=None):
        self._escopo = uuid.uuid1() if escopo == None else escopo
        self._pai = pai
        self._registros = []

    def retornaEscopo(self) -> str:
        return self._escopo

    def retornaPai(self):
        return self._pai

    def verificaRegistroExisteTabelaAtual(self, ident):
        return next((item for item in self._registros if item["ident"] == ident), None)

    def registraVariavel(self, tipo, ident, valor=None):
        if self.verificaRegistroExisteTabelaAtual(ident) == None:
            registro = {'tipo_registro': 'variavel', 'tipo': tipo, 'ident': ident, 'valor': valor}
            self._registros.append(registro)

    def registraFuncao(self, tipo, ident, parametros=None):
        if self.verificaRegistroExisteTabelaAtual(ident) == None:
            registro = {'tipo_registro': 'funcao', 'tipo': tipo, 'ident': ident, 'parametros': parametros}
            self._registros.append(registro)

    def retornaRegistro(self, ident):
        registro = next((item for item in self._registros if item["ident"] == ident), None)
        if registro:
            return registro
        if self.retornaPai():
            registro = self.retornaPai().retornaRegistro(ident)
        return  registro if registro else None