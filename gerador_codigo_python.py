from componentes_parser.no import No
from componentes_parser.op_bin import OpBin
from componentes_parser.numero import Numero
from componentes_parser.texto import Texto
from componentes_parser.variavel import Variavel
from componentes_parser.instrucao import Instrucao
import componentes_lexer.op_aritmetico as op_arit
import componentes_lexer.op_relational as op_rel
from gerador_codigo import GeradorDeCodigo
import componentes_lexer.valores as lexer_valores
import componentes_lexer.palavras_chaves as lexer_palavras_chave
from token_ import Token
from componentes_parser.declaracao_variavel import DeclaracaoVariavel

class GeradorDeCodigoParaPython(GeradorDeCodigo):
    def gera_estrutura_base(self):
        pass

    def gera_instrucoes(self, no_instrucoes:Instrucao):
        instrucoes_txt = "\n"
        for inst in no_instrucoes.retornaInstrucoes():
            res = self.gera_instrucao(inst)
            instrucoes_txt += f"{res}\n"
        return instrucoes_txt

    def gera_instrucao(self, no):
        if isinstance(no, DeclaracaoVariavel):
            return self.gera_decl_var(no)

    def gera_decl_var(self, no: DeclaracaoVariavel):
        ident = no.retornaIdentificador().retornaValor()
        expr = self.gera_expr(no.retornaValor(), "")
        return f"{ident} = {expr}"

    def gera_expr(self, no:No, saida:str):
        if isinstance(no, OpBin):
            op = self.gera_operador(no.retornaOp().retornaValor())
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