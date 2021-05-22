import constantes
from token_ import Token
from posicao import Posicao

class Lexer:
    _texto = ''
    _indiceAtual = 0
    _carac_atual = ''
    _linha = 0
    _coluna = 0
    _tokens = []
    def __init__(self, texto):
        self._texto = texto
        self._carac_atual = texto[self._indiceAtual]

    def __adicionaToken(self, id, val):
        pos = self.__retornaPosicaoAtual()
        token = Token(id, val, pos)
        self._tokens.append(token)

    def __retornaCaracterAtual(self, i = 0):
        if self._indiceAtual < len(self._texto):
            return  self._texto[self._indiceAtual + i]
        else:
            return None

    def __retornaPosicaoAtual(self):
        return Posicao(self._linha, self._coluna)

    def __avancaColuna(self):
        if len(self._texto) > self._indiceAtual:
            self._indiceAtual += 1
            self._coluna += 1
        # Se encontrar uma quebra de linha, avança uma linha
        if self.__retornaCaracterAtual() == '\\' and self.__retornaCaracterAtual(1) == 'n':
            self.__avancaLinha()

    def __avancaLinha(self):
        self._coluna = 0
        self._linha += 1

    def __EOF(self):
        return self.__retornaCaracterAtual() == None

    def __retornaIdentificador(self):
        pass

    def __retornaNumero(self):
        pass

    def retornaTokens(self):
        while not self.__EOF():
            if self.__retornaCaracterAtual() in ' \t':
                self.__avancaColuna()
            elif self.__retornaCaracterAtual() in constantes.caracteres:
                ident = self.__retornaIdentificador()
                self.__adicionaToken(constantes.t_identificador, ident)
            elif self.__retornaCaracterAtual() in constantes.digitos:
                num = self.__retornaNumero()
                self.__adicionaToken(constantes.t_numero, num)
            self.__avancaColuna()