from lexer import Lexer

arq = open("teste.lpb", "r", encoding='utf-8')
conteudo = arq.read()
lexer = Lexer(conteudo)
tokens = lexer.retornaTokens()
for tkn in tokens:
    print(tkn)