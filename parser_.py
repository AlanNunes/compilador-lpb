from componentes_parser.repita_ate import RepitaAte
from componentes_parser.repita_id_ate import RepitaIdentAte
from componentes_parser.repita_com_cond import RepitaComCond
from componentes_parser.senaose import SenaoSe
from typing import List
from componentes_parser.no import No
from componentes_parser.erros.sintaxe_erro import ErroSintaxe
from componentes_parser.erros.erro import Erro
from componentes_parser.se import Se
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
        self._erros = []

    def parse(self) -> No:
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

    def __registraErro(self, erro: Erro):
        self._erros.append(erro)

    def retornaErros(self) -> List[Erro]:
        return self._erros

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
        operadores = [op_arit.mult, op_arit.div, op_arit.pot, op_rel.maior_que, op_rel.menor_que, op_rel.maior_igual, op_rel.menor_igual]
        while tkn_atual.retornaTipo() in operadores:
            tkn_op = self.__retornaTokenAtual()
            self.__avancaToken()
            fat_dir = self.__parseFator()
            fat_esq = OpBin(esq=fat_esq, op=tkn_op, dir=fat_dir)
            tkn_atual = self.__retornaTokenAtual()
        return fat_esq

    def __parseExpr(self):
        fat_esq = self.__parseTermo()
        tkn_atual = self.__retornaTokenAtual()
        while tkn_atual.retornaTipo() in [op_arit.sub, op_arit.soma, op_rel.igualdade]:
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

    def __parseSenaoSe(self) -> Se:
        if self.__retornaTokenAtual().retornaTipo() == palavras_chaves.senaose:
            self.__avancaToken()
        cond = self.__parseExpr()
        if self.__retornaTokenAtual().retornaTipo() == palavras_chaves.entao:
            self.__avancaToken()
        else:
            msgErro = f"Espera-se '{palavras_chaves.entao}' ao invés de '{self.__retornaTokenAtual().retornaTipo()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
            self.__avancaToken()
        instrucoes = []
        while self.__retornaTokenAtual().retornaTipo() not in [palavras_chaves.senao, palavras_chaves.senaose, palavras_chaves.fim_se]:
            instrucoes.append(self.__parseInstrucao())
        senaose = None
        senao = None
        if self.__retornaTokenAtual().retornaTipo() == palavras_chaves.senaose:
            senaose = self.__parseSenaoSe()
        elif self.__retornaTokenAtual().retornaTipo() == palavras_chaves.senao:
            senao = self.__parseInstrucao()
        return SenaoSe(cond=cond, corpo=instrucoes, senaose=senaose, senao=senao)
        

    def __parseSe(self) -> Se:
        if self.__retornaTokenAtual().retornaTipo() == palavras_chaves.se:
            self.__avancaToken()
        cond = self.__parseExpr()
        if self.__retornaTokenAtual().retornaTipo() == palavras_chaves.entao:
            self.__avancaToken()
        else:
            msgErro = f"Espera-se '{palavras_chaves.entao}' ao invés de '{self.__retornaTokenAtual().retornaTipo()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
            self.__avancaToken()
        instrucoes = []
        while self.__retornaTokenAtual().retornaTipo() not in [palavras_chaves.senao, palavras_chaves.senaose, palavras_chaves.fim_se]:
            instrucoes.append(self.__parseInstrucao())
        senaose = None
        senao = None
        if self.__retornaTokenAtual().retornaTipo() == palavras_chaves.senaose:
            senaose = self.__parseSenaoSe()
        elif self.__retornaTokenAtual().retornaTipo() == palavras_chaves.senao:
            senao = self.__parseInstrucao()
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.fim_se:
            msgErro = f"Espera-se '{palavras_chaves.fim_se}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        self.__avancaToken()
        return Se(cond=cond, corpo=instrucoes, senaose=senaose, senao=senao)

    def __parseRepitaAte(self):
        expr = self.__parseExpr()
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.entao:
            msgErro = f"Espera-se '{palavras_chaves.entao}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        self.__avancaToken()
        instrucoes = []
        while self.__retornaTokenAtual().retornaTipo() not in [palavras_chaves.fim_repita, tipos_tokens.EOF]:
            instrucoes.append(self.__parseInstrucao())
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.fim_repita:
            msgErro = f"Espera-se '{palavras_chaves.fim_repita}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        return RepitaAte(expr=expr, instrucoes=instrucoes)

    def __parseRepitaIdentAte(self):
        ident = Variavel(self.__retornaTokenAtual())
        self.__avancaToken()
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.ate:
            msgErro = f"Espera-se '{palavras_chaves.ate}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        self.__avancaToken()
        expr = self.__parseExpr()
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.entao:
            msgErro = f"Espera-se '{palavras_chaves.entao}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        self.__avancaToken()
        instrucoes = []
        while self.__retornaTokenAtual().retornaTipo() not in [palavras_chaves.fim_repita, tipos_tokens.EOF]:
            instrucoes.append(self.__parseInstrucao())
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.fim_repita:
            msgErro = f"Espera-se '{palavras_chaves.fim_repita}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        return RepitaIdentAte(ident=ident, expr=expr, instrucoes=instrucoes)

    def __parseRepitaComCond(self):
        decl_var = self.__parseDeclaracaoVariavel()
        if self.__retornaTokenAtual().retornaTipo() != tipos_tokens.delimitador:
            msgErro = f"Espera-se '{tipos_tokens.delimitador}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
            self.__avancaToken()
        self.__avancaToken()
        cond = self.__parseExpr()
        if self.__retornaTokenAtual().retornaTipo() != tipos_tokens.delimitador:
            msgErro = f"Espera-se '{tipos_tokens.delimitador}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
            self.__avancaToken()
        self.__avancaToken()
        atrib_var = self.__parseAtribuicaoVariavel()
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.entao:
            msgErro = f"Espera-se '{palavras_chaves.entao}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        self.__avancaToken()
        instrucoes = []
        while self.__retornaTokenAtual().retornaTipo() not in [palavras_chaves.fim_repita, tipos_tokens.EOF]:
            instrucoes.append(self.__parseInstrucao())
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.fim_repita:
            msgErro = f"Espera-se '{palavras_chaves.fim_repita}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        return RepitaComCond(decl_var=decl_var, cond=cond, atrib_var=atrib_var, instrucoes=instrucoes)

    def __parseRepita(self):
        if self.__retornaTokenAtual().retornaTipo() != palavras_chaves.repita:
            msgErro = f"Espera-se '{palavras_chaves.repita}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
        self.__avancaToken()
        token_atual = self.__retornaTokenAtual()
        if token_atual.retornaTipo() == palavras_chaves.ate:
            self.__avancaToken()
            return self.__parseRepitaAte()
        elif token_atual.retornaTipo() == tipos_tokens.identificador:
            return self.__parseRepitaIdentAte()
        elif token_atual.retornaTipo() in [palavras_chaves.tipo_flutuante, palavras_chaves.tipo_inteiro]:
            return self.__parseRepitaComCond()
        else:
            msgErro = f"Espera-se '{palavras_chaves.tipo_inteiro} ou {palavras_chaves.tipo_flutuante}' ao invés de '{self.__retornaTokenAtual().retornaValor()}'."
            posErro = self.__retornaTokenAtual().retornaPosicao()
            self.__registraErro(ErroSintaxe(msg=msgErro, pos=posErro))
            self.__avancaToken()

    def __parseInstrucao(self):
        tkn_atual = self.__retornaTokenAtual()
        if tkn_atual.retornaTipo() in palavras_chaves.todos_tipos_decl_var:
            return self.__parseDeclaracaoVariavel()
        elif tkn_atual.retornaTipo() == tipos_tokens.identificador:
            prox_tkn = self.__retornaTokenAtual(1)
            if prox_tkn.retornaTipo() == op_arit.op_atribuicao:
                return self.__parseAtribuicaoVariavel()
        elif tkn_atual.retornaTipo() == palavras_chaves.se:
            return self.__parseSe()
        elif tkn_atual.retornaTipo() == palavras_chaves.repita:
            return self.__parseRepita()
        elif tkn_atual.retornaTipo() in [valores.texto, valores.inteiro, valores.flutuante, op_arit.parent_esq, tipos_tokens.identificador]:
            return self.__parseExpr()
        else:
            self.__avancaToken()
            return None