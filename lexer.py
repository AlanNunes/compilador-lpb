import componentes_lexer.valores as valores
import componentes_lexer.tipos_tokens as tipos_tokens
import componentes_lexer.palavras_chaves as palavras_chaves
import componentes_lexer.op_relational as op_rel
import componentes_lexer.op_aritmetico as op_arit
from componentes_lexer.posicao import Posicao
from token_ import Token

# O Lexer é responsável por ler todo o código-fonte
#  e transformar cada pedaço em um Token que será
#  utilizado no Parser para montar a árvore de sintáxe
#  abstrata e realizar validações como análise sintática
#  e análise semântica.
class Lexer:
    _texto = ''
    _indiceAtual = 0
    _carac_atual = ''
    _linha = 1
    _coluna = 1
    _tokens = []
    def __init__(self, texto):
        self._texto = texto
        self._carac_atual = texto[self._indiceAtual]

    # Adiciona um token à lista de tokens gerados
    #  durante a leitura do código fonte.
    def __adicionaToken(self, token: Token):
        self._tokens.append(token)

    # Retorna o caracter atual a ser lido.
    def __retornaCaracterAtual(self, i = 0):
        if self._indiceAtual + i < len(self._texto):
            return  self._texto[self._indiceAtual + i]
        else:
            return None

    # Retorna a posição atual de leitura.
    # Exemplo: coluna 20 e linha 10.
    def __retornaPosicaoAtual(self) -> Posicao:
        return Posicao(self._linha, self._coluna)

    # Avança um caracter (ou coluna).
    def __avancaColuna(self):
        c_atual = self.__retornaCaracterAtual() 
        # Se encontrar uma quebra de linha, avança uma linha.
        if c_atual == '\n':
            self.__avancaLinha()
        if len(self._texto) > self._indiceAtual:
            self._indiceAtual += 1
            self._coluna += 1

    # Pula para a próxima linha do código fonte.
    def __avancaLinha(self):
        self._coluna = 0
        self._linha += 1

    # Retorna verdadeiro se já tiver lido todo código fonte.
    def __EOF(self) -> bool:
        return self.__retornaCaracterAtual() == None

    # Retorna um identificador.
    # Exemplo: o nome de uma variável.
    def __retornaIdentificador(self) -> Token:
        valor = ''
        pos = self.__retornaPosicaoAtual()
        while not self.__EOF() and self.__retornaCaracterAtual() in valores.caracteres:
            valor += self.__retornaCaracterAtual()
            self.__avancaColuna()
        if valor in palavras_chaves.todas:
            p_chave = palavras_chaves.retornaPalavraChave(valor)
            return Token(p_chave, pos)
        return Token(tipos_tokens.identificador, pos, valor)

    # Retorna um token de valor de texto
    # Exemplo: 10
    def __retornaNumero(self) -> Token:
        valor = ''
        pos = self.__retornaPosicaoAtual()
        while not self.__EOF() and self.__retornaCaracterAtual() in valores.valor_numerico:
            valor += self.__retornaCaracterAtual()
            self.__avancaColuna()
        try:
            int(valor)
            return Token(valores.inteiro, pos, valor)
        except:
            return Token(valores.flutuante, pos, valor)

    # Retorna um token de valor de texto
    # Exemplo "Olá mundo!"
    def __retornaTexto(self) -> Token:
        valor = ''
        pos = self.__retornaPosicaoAtual()
        tipo = valores.texto
        self.__avancaColuna()
        while not self.__EOF() and self.__retornaCaracterAtual() in valores.valor_texto and self.__retornaCaracterAtual() != "\"":
            valor += self.__retornaCaracterAtual()
            self.__avancaColuna()
        if self.__retornaCaracterAtual() == "\"":
            self.__avancaColuna()
        return Token(tipo, pos, valor)

    # Retorna um token do tipo operador relacional
    def __retornaOperadorRelacional(self) -> Token:
        pos = self.__retornaPosicaoAtual()
        operador = self.__retornaCaracterAtual()
        if operador + self.__retornaCaracterAtual(1) in op_rel.todos:
            self.__avancaColuna()
            operador = operador + self.__retornaCaracterAtual()
            self.__avancaColuna()
        if operador == '>':
            return Token(op_rel.maior_que, pos)
        elif operador == '<':
            return Token(op_rel.menor_que, pos)
        elif operador == '>=':
            return Token(op_rel.maior_igual, pos)
        elif operador == '<=':
            return Token(op_rel.menor_igual, pos)
        elif operador == '==':
            return Token(op_rel.igualdade, pos)
        elif operador == '!=':
            return Token(op_rel.desigualdade, pos)

    # Retorna um token do tipo aritimético
    def __retornaOperadorAritmetico(self) -> Token:
        operador = self.__retornaCaracterAtual()
        pos = self.__retornaPosicaoAtual()
        if operador == '+':
            self.__avancaColuna()
            return Token(op_arit.soma, pos)
        elif operador == '/':
            self.__avancaColuna()
            return Token(op_arit.div, pos)
        elif operador == '*':
            self.__avancaColuna()
            return Token(op_arit.mult, pos)
        elif operador == '=':
            self.__avancaColuna()
            return Token(op_arit.op_atribuicao, pos)
        elif operador == '^':
            self.__avancaColuna()
            return Token(op_arit.pot, pos)
        elif operador == '(':
            self.__avancaColuna()
            return Token(op_arit.parent_esq, pos)
        elif operador == ')':
            self.__avancaColuna()
            return Token(op_arit.parent_dir, pos)

    # Realiza o 'tokenize' e retorna uma lista de tokens
    #  gerados através do código fonte em lpb.
    def retornaTokens(self) -> list:
        while not self.__EOF():
            caracter_atual = self.__retornaCaracterAtual()
            caracter_posterior = self.__retornaCaracterAtual(1)
            if caracter_atual in ' \t':
                self.__avancaColuna()
            elif caracter_atual in valores.caracteres:
                tkn_ident = self.__retornaIdentificador()
                self.__adicionaToken(tkn_ident)
            elif caracter_atual in valores.digitos:
                tkn_num = self.__retornaNumero()
                self.__adicionaToken(tkn_num)
            elif caracter_atual == "\"":
                tkn_texto = self.__retornaTexto()
                self.__adicionaToken(tkn_texto)
            elif caracter_atual in op_rel.todos or (caracter_posterior != None and caracter_atual + caracter_posterior in op_rel.todos):
                tkn_op_rel = self.__retornaOperadorRelacional()
                self.__adicionaToken(tkn_op_rel)
            elif caracter_atual in op_arit.todos:
                tkn_op_arit = self.__retornaOperadorAritmetico()
                self.__adicionaToken(tkn_op_arit)
            elif caracter_atual == '.':
                pos = self.__retornaPosicaoAtual()
                tkn_ponto = Token(tipos_tokens.ponto, pos)
                self.__adicionaToken(tkn_ponto)
                self.__avancaColuna()
            else:
                self.__avancaColuna()
        self.__adicionaToken(Token(tipos_tokens.EOF, self.__retornaPosicaoAtual()))
        return self._tokens