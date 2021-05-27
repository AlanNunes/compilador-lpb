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
if len(erros) > 0:
    print('O código fonte possui erros, confira-os acima.')
else:
    print('O projeto foi compilado com sucesso!')