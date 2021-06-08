from os import error
from lexer import Lexer
from parser_ import Parser
from gerador_codigo_python import GeradorDeCodigoParaPython
import sys
import os

print('============================================================')
print('# LINGUAGEM DE PROGRAMAÇÃO BRASILEIRA - LPB        ')
print('# Repositório: https://github.com/AlanNunes/compilador-lpb')
print('# Autor: Alan Nunes (https://github.com/AlanNunes)')
print('============================================================')
try:
    if len(sys.argv) <= 1:
        print('Você precisa passar o nome do arquivo como argumento.')
    else:
        nome_arquivo = sys.argv[1]
        arq = open(nome_arquivo, "r", encoding='utf-8')
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
            gerador_python = GeradorDeCodigoParaPython()
            res = gerador_python.gera_instrucoes(ast)
            f = open("output.py", "w", encoding='utf-8')
            f.write(res)
            f.close()
            print('O projeto foi compilado com sucesso!')
            print('Executando programa...\n')
            os.system('python output.py')
        
except FileNotFoundError:
    print(f'Arquivo {nome_arquivo} não encontrado!')