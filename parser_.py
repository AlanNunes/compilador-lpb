from componentes_parser.variavel import Variavel
from componentes_parser.atribuicao_variavel import AtribuicaoVariavel
from componentes_parser.declaracao_variavel import DeclaracaoVariavel
from componentes_parser.instrucao import Instrucao
from token_ import Token
from componentes_parser.texto import Texto
from componentes_parser.op_bin import OpBin
import componentes_lexer.valores as valores
import componentes_lexer.tipos_tokens as tipos_tokens
import componentes_lexer.palavras_chaves as palavras_chaves
import componentes_lexer.op_relational as op_rel
import componentes_lexer.op_aritmetico as op_arit
from componentes_lexer.posicao import Posicao

from componentes_parser.numero import Numero

class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._ind_tkn = 0

    def parse(self):
        instrucoes = Instrucao()
        tkn_atual = self.__retornaTokenAtual()
        while tkn_atual.retornaTipo() != tipos_tokens.EOF:
            inst = self.__parseInstrucao()
            if inst != None:
                instrucoes.adicionaInstrucao(inst)
            tkn_atual = self.__retornaTokenAtual()
        return instrucoes

    def __avancaToken(self):
        qnt_tokens = len(self._tokens) - 1
        if self._ind_tkn < qnt_tokens:
            self._ind_tkn += 1

    def __retornaTokenAtual(self, i=0) -> Token:
        if self._ind_tkn + i < len(self._tokens):
            return self._tokens[self._ind_tkn + i]
        else:
            return None

    def __parseFator(self):
        tkn_atual = self.__retornaTokenAtual()
        if tkn_atual.retornaTipo() in [valores.inteiro, valores.flutuante]:
            self.__avancaToken()
            return Numero(tkn_atual)
        elif tkn_atual.retornaTipo() == valores.texto:
            self.__avancaToken()
            return Texto(tkn_atual)
        elif tkn_atual.retornaTipo() == tipos_tokens.identificador:
            prox_tkn = self.__retornaTokenAtual(1)
            if prox_tkn.retornaTipo() == op_arit.parent_esq:
                return self.__parseFuncao()
            self.__avancaToken()
            return Variavel(tkn_atual)
        elif tkn_atual.retornaTipo() == op_arit.parent_esq:
            self.__avancaToken()
            expr = self.__parseExpr()
            self.__avancaToken()
            return expr 

    def __parseTermo(self):
        fat_esq = self.__parseFator()
        tkn_atual = self.__retornaTokenAtual()
        while tkn_atual.retornaTipo() in [op_arit.mult, op_arit.div, op_arit.pot]:
            tkn_op = self.__retornaTokenAtual()
            self.__avancaToken()
            fat_dir = self.__parseFator()
            fat_esq = OpBin(esq=fat_esq, op=tkn_op, dir=fat_dir)
            tkn_atual = self.__retornaTokenAtual()
        return fat_esq

    def __parseExpr(self):
        fat_esq = self.__parseTermo()
        tkn_atual = self.__retornaTokenAtual()
        while tkn_atual.retornaTipo() in [op_arit.sub, op_arit.soma]:
            tkn_op = self.__retornaTokenAtual()
            self.__avancaToken()
            fat_dir = self.__parseTermo()
            fat_esq = OpBin(esq=fat_esq, op=tkn_op, dir=fat_dir)
            tkn_atual = self.__retornaTokenAtual()
        return fat_esq

    def __parseDeclaracaoVariavel(self):
        tkn_tipo_var = self.__retornaTokenAtual()
        self.__avancaToken()
        ident_var = self.__retornaTokenAtual()
        self.__avancaToken()
        # TODO: lançar exceção se não tiver o token de atribuição '='
        self.__avancaToken()
        valor = self.__parseExpr()
        return DeclaracaoVariavel(tipo=tkn_tipo_var, ident=ident_var, val=valor)

    def __parseAtribuicaoVariavel(self):
        ident_var = self.__retornaTokenAtual()
        self.__avancaToken()
        op = self.__retornaTokenAtual()
        # TODO: lançar exceção se não tiver o token de atribuição '='
        self.__avancaToken()
        valor = self.__parseExpr()
        return AtribuicaoVariavel(ident=ident_var, op=op, val=valor)

    def __parseFuncao(self):
        pass

    def __parseInstrucao(self):
        tkn_atual = self.__retornaTokenAtual()
        if tkn_atual.retornaTipo() in palavras_chaves.todos_tipos_decl_var:
            return self.__parseDeclaracaoVariavel()
        elif tkn_atual.retornaTipo() == tipos_tokens.identificador:
            prox_tkn = self.__retornaTokenAtual(1)
            if prox_tkn.retornaTipo() == op_arit.op_atribuicao:
                return self.__parseAtribuicaoVariavel()
        elif tkn_atual.retornaTipo() in [valores.texto, valores.inteiro, valores.flutuante, op_arit.parent_esq]:
            return self.__parseExpr()