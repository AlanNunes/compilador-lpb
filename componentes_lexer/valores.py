import string

# Representa os caracteres aceitos durante no lexer
caracteres = string.ascii_letters + 'ãâáàéèêíìîçõóòôúùûÃÂÁÀÉÈÊÍÌÎÇÕÓÒÔÚÙÛ'
# Representa os dígitos aceitos durante no lexer
digitos = string.digits
# Lista de operadores relacionais aceitos no lexer
op_relacionais = ['>', '<', '>=', '<=', '==', '!=']
# Representa os dígitos e pontuação aceitos durante no lexer para formar um valor numérico.
valor_numerico = digitos + '.'
# Representa tudo aceita na formação de um texto (string)
valor_texto = caracteres + ' '

# Representa que o valor do token é inteiro
inteiro = 'inteiro'
# Representa que o valor do token é flutuante
flutuante = 'flutuante'
# Representa que o valor do token é um texto
texto = 'texto'
# Representa um valor númerico
numero = 'numero'