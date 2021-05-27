from os import error
from lexer import Lexer
from parser_ import Parser

arq = open("teste.lpb", "r", encoding='utf-8')
conteudo = arq.read()
lexer = Lexer(conteudo)
tokens = lexer.retornaTokens()
parser = Parser(tokens)
ast = parser.parse()
erros = parser.retornaErros()
for e in erros:
    print(e.retornaErro())