from lexer import Lexer

arq = open("teste.lpb", "r")
conteudo = arq.read()
lexer = Lexer(conteudo)
tokens = lexer.retornaTokens()