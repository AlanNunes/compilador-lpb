import componentes_lexer.valores as valores
from componentes_parser.boleano import Boleano
import componentes_lexer.funcoes_internas as funcoes_internas
from componentes_parser.chamada_funcao import ChamadaFuncao
from componentes_parser.parametro import Parametro
from componentes_parser.retorna import Retorna
from componentes_parser.funcao import Funcao
from componentes_parser.repita_com_cond import RepitaComCond
from componentes_parser.repita_id_ate import RepitaIdentAte
from componentes_parser.repita_ate import RepitaAte
from componentes_parser.repita import Repita
from componentes_parser.atribuicao_variavel import AtribuicaoVariavel
from typing import List
from componentes_parser.no import No
from componentes_parser.op_bin import OpBin
from componentes_parser.numero import Numero
from componentes_parser.texto import Texto
from componentes_parser.variavel import Variavel
from componentes_parser.instrucao import Instrucao
from componentes_parser.se import Se
from componentes_parser.senaose import SenaoSe
import componentes_lexer.op_aritmetico as op_arit
import componentes_lexer.op_relational as op_rel
from gerador_codigo import GeradorDeCodigo
from token_ import Token
from componentes_parser.declaracao_variavel import DeclaracaoVariavel

class GeradorDeCodigoParaPython(GeradorDeCodigo):
    def __init__(self):
        # Representa a quantidade de Tabs (\t)
        self._identacao_atual = 0

    def __avancaIdentacao(self):
        self._identacao_atual += 1

    def __recuaIdentacao(self):
        self._identacao_atual -= 1

    def __retornaIdentacaoAtual(self):
        return self._identacao_atual * "\t"

    def gera_estrutura_base(self):
        pass

    def gera_instrucoes(self, no_instrucoes:Instrucao):
        instrucoes_txt = ""
        instrucoes = no_instrucoes.retornaInstrucoes()
        for inst in instrucoes:
            res = self.gera_instrucao(inst)
            instrucoes_txt += f"{res}\n"
        return instrucoes_txt

    def gera_instrucao(self, no):
        if isinstance(no, DeclaracaoVariavel):
            return self.gera_decl_var(no)
        elif isinstance(no, AtribuicaoVariavel):
            return self.gera_atr_var(no)
        elif isinstance(no, Se):
            return self.gera_se(no)
        elif isinstance(no, Repita):
            return self.gera_repita(no)
        elif isinstance(no, Funcao):
            return self.gera_funcao(no)
        elif isinstance(no, Retorna):
            return self.gera_retorne(no)
        elif isinstance(no, ChamadaFuncao):
            return self.gera_chamada_funcao(no)

    def gera_chamada_interna_leia(self, parametros: List):
        identacao = self.__retornaIdentacaoAtual()
        valor = ''
        for param in parametros:
            expr = self.gera_expr(param, '')
            valor += f"{expr} "
        valor = valor[:-1]
        return f"{identacao}input({valor})"

    def gera_chamada_interna_escreva(self, parametros: List):
        identacao = self.__retornaIdentacaoAtual()
        valor = ''
        for param in parametros:
            expr = self.gera_expr(param, '')
            valor += f"{expr} "
        valor = valor[:-1]
        return f"{identacao}print({valor})"

    def gera_chamada_interna_conv_para_flutuante(self, expr: No):
        expressao = self.gera_expr(expr, '')
        return f"float({expressao})"

    def gera_chamada_interna_conv_para_inteiro(self, expr: No):
        expressao = self.gera_expr(expr, '')
        return f"int({expressao})"

    def gera_chamada_interna_conv_para_texto(self, expr: No):
        expressao = self.gera_expr(expr, '')
        return f"str({expressao})"

    def gera_chamada_funcao_interna(self, no: ChamadaFuncao):
        ident = no.retornaIdentificador().retornaValor()
        parametros = no.retornaParametros()
        if ident == funcoes_internas.escreva:
            return self.gera_chamada_interna_escreva(parametros)
        elif ident == funcoes_internas.leia:
            return self.gera_chamada_interna_leia(parametros)
        elif ident == funcoes_internas.converte_para_flutuante:
            return self.gera_chamada_interna_conv_para_flutuante(parametros[0])
        elif ident == funcoes_internas.converte_para_inteiro:
            return self.gera_chamada_interna_conv_para_inteiro(parametros[0])
        elif ident == funcoes_internas.converte_para_texto:
            return self.gera_chamada_interna_conv_para_texto(parametros[0])

    def gera_parametros_chamada_funcao(self, parametros: List):
        res = ''
        for param in parametros:
            expr = self.gera_expr(param, '')
            res += f"{expr},"
        return res[:-1]

    def gera_chamada_funcao(self, no: ChamadaFuncao, com_identacao=True):
        if no.retornaIdentificador().retornaValor() in funcoes_internas.funcoes_internas:
            return self.gera_chamada_funcao_interna(no)
        identacao = self.__retornaIdentacaoAtual() if com_identacao else ''
        ident = no.retornaIdentificador().retornaValor()
        parametros = self.gera_parametros_chamada_funcao(no.retornaParametros())
        return f"{identacao}{ident}({parametros})"

    def gera_retorne(self, no: Retorna):
        identacao = self.__retornaIdentacaoAtual()
        expr = self.gera_expr(no.retornaExpr(), '')
        return f"{identacao}return {expr}"

    def gera_parametros(self, no: List[Parametro]):
        res = ''
        for param in no:
            nome = param.retornaIdentificador().retornaValor()
            expr = self.gera_expr(param.retornaValor(), '')
            if expr:
                res += f"{nome} = {expr},"
            else:
                res += f"{nome},"
        return res[:-1]

    def gera_funcao(self, no: Funcao):
        identacao = self.__retornaIdentacaoAtual()
        nome = no.retornaIdentificador().retornaValor()
        parametros = self.gera_parametros(no.retornaParametros())
        self.__avancaIdentacao()
        instrucoes = self.gera_instrucoes(no.retornaInstrucao())
        self.__recuaIdentacao()
        return f"{identacao}def {nome}({parametros}):\n{instrucoes}"

    def gera_repita(self, no: Repita):
        if isinstance(no, RepitaAte):
            return self.gera_repita_ate(no)
        elif isinstance(no, RepitaIdentAte):
            return self.gera_repita_ident_ate(no)
        elif isinstance(no, RepitaComCond):
            return self.gera_repita_com_cond(no)

    def gera_repita_ate(self, no: RepitaAte):
        identacao = self.__retornaIdentacaoAtual()
        expr = self.gera_expr(no.retornaExpr(), '')
        self.__avancaIdentacao()
        instrucoes = self.gera_instrucoes(no.retornaInstrucoes())
        self.__recuaIdentacao()
        return f"{identacao}for i in range({expr}):\n{instrucoes}"

    def gera_repita_ident_ate(self, no: RepitaIdentAte):
        identacao = self.__retornaIdentacaoAtual()
        ident = self.gera_expr(no.retornaIdentificador(), '')
        expr = self.gera_expr(no.retornaExpr(), '')
        self.__avancaIdentacao()
        instrucoes = self.gera_instrucoes(no.retornaInstrucoes())
        self.__recuaIdentacao()
        return f"{identacao}for {ident} in range({expr}):\n{instrucoes}"

    def gera_repita_com_cond(self, no: RepitaComCond):
        identacao = self.__retornaIdentacaoAtual()
        decl_var = self.gera_decl_var(no.retornaDeclVar())
        cond = self.gera_expr(no.retornaCond(), '')
        self.__avancaIdentacao()
        instrucoes = self.gera_instrucoes(no.retornaInstrucoes())
        self.__recuaIdentacao()
        res = f'{identacao}{decl_var}\n'
        res += f'{identacao}while {cond}:\n{instrucoes}'
        return res

    def gera_se(self, no:Se):
        identacao = self.__retornaIdentacaoAtual()
        cond = self.gera_expr(no.retornaCond(), '')
        self.__avancaIdentacao()
        instrucoes_corpo = no.retornaCorpo()
        corpo = self.gera_instrucoes(instrucoes_corpo)
        self.__recuaIdentacao()
        senaose = None
        senao = None
        if no.retornaSenaoSe():
            senaose = self.gera_senaose(no.retornaSenaoSe())
        if no.retornaSenao():
            senao = self.gera_senao(no.retornaSenao())
        if senaose and senao:
            return f"{identacao}if {cond}:\n{corpo}{senaose}\n{senao}"
        elif senaose:
            return f"{identacao}if {cond}:\n{corpo}{senaose}"
        elif senao:
            return f"{identacao}if {cond}:\n{corpo}{senao}"
        else:
            return f"{identacao}if {cond}:\n{corpo}"

    def gera_senaose(self, no:SenaoSe):
        identacao = self.__retornaIdentacaoAtual()
        cond = self.gera_expr(no.retornaCond(), '')
        self.__avancaIdentacao()
        instrucoes_corpo = no.retornaCorpo()
        corpo = self.gera_instrucoes(instrucoes_corpo)
        self.__recuaIdentacao()
        senaose = None
        senao = None
        if no.retornaSenaoSe():
            senaose = self.gera_senaose(no.retornaSenaoSe())
        elif no.retornaSenao():
            senao = self.gera_senao(no.retornaSenao())
        if senaose and senao:
            return f"{identacao}elif {cond}:\n{corpo}{senaose}\n{senao}"
        elif senaose:
            return f"{identacao}elif {cond}:\n{corpo}{senaose}"
        elif senao:
            return f"{identacao}elif {cond}:\n{corpo}{senao}"
        else:
            return f"{identacao}elif {cond}:\n{corpo}"

    def gera_senao(self, no:Instrucao):
        identacao = self.__retornaIdentacaoAtual()
        self.__avancaIdentacao()
        instrucoes = self.gera_instrucoes(no)
        self.__recuaIdentacao()
        return f"{identacao}else:\n{instrucoes}"

    def gera_decl_var(self, no: DeclaracaoVariavel):
        identacao = self.__retornaIdentacaoAtual()
        ident = no.retornaIdentificador().retornaValor()
        expr = self.gera_expr(no.retornaValor(), "")
        return f"{identacao}{ident} = {expr}"

    def gera_atr_var(self, no: AtribuicaoVariavel):
        identacao = self.__retornaIdentacaoAtual()
        ident = no.retornaIdentificador().retornaValor()
        expr = self.gera_expr(no.retornaValor(), "")
        return f"{identacao}{ident} = {expr}"

    def gera_expr(self, no:No, saida:str):
        if isinstance(no, OpBin):
            op = self.gera_operador(no.retornaOp())
            esq_res = self.gera_expr(no.retornaEsq(), saida)
            dir_res = self.gera_expr(no.retornaDir(), saida)
            saida += f"({esq_res} {op} {dir_res})"
            return saida
        elif isinstance(no, Numero):
            saida += f"{no.retornaValor()}"
            return saida
        elif isinstance(no, Variavel):
            saida += f"{no.retornaValor()}"
            return saida
        elif isinstance(no, Texto):
            saida += f"\"{no.retornaValor()}\""
            return saida
        elif isinstance(no, Boleano):
            return "True" if no.retornaValor() == valores.verdadeiro else "False"
        elif isinstance(no, ChamadaFuncao):
            return self.gera_chamada_funcao(no, com_identacao=False)

    def gera_operador(self, token:Token):
        if token.retornaTipo() == op_arit.soma:
            return "+"
        elif token.retornaTipo() == op_arit.sub:
            return "-"
        elif token.retornaTipo() == op_arit.mult:
            return "*"
        elif token.retornaTipo() == op_arit.div:
            return "/"
        elif token.retornaTipo() == op_rel.maior_que:
            return ">"
        elif token.retornaTipo() == op_rel.menor_que:
            return "<"
        elif token.retornaTipo() == op_rel.maior_igual:
            return ">="
        elif token.retornaTipo() == op_rel.menor_igual:
            return "<="
        elif token.retornaTipo() == op_rel.igualdade:
            return "=="