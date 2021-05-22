import string

# Representa os caracteres aceitos durante no lexer
caracteres = string.ascii_letters
# Representa os dígitos aceitos durante no lexer
digitos = string.digits

# Representa que o valor do token é inteiro
t_int = 'int'
# Representa que o valor do token é flutuante
t_flutuante = 'flutuante'
# Representa que o valor do token é um texto
t_texto = 'texto'

# Reperesenta um identificador
t_identificador = 'identificador'
# Representa um valor númerico
t_numero = 'numero'

# Representa o sinal de soma
t_soma = 'soma'
# Representa o sinal de divisão
t_div = 'div'
# Representa o sinal de multiplicação
t_mult = 'mult'
# Representa o sinal de potência '^'
t_pot = 'pot'

# Representa o sinal parêntese esquerdo
t_parent_esq = 'parent_esq'
# Representa o sinal parêntese direito
t_parent_dir = 'parent_dir'

# Representa o sinal de igualdade '=='
t_igualdade = 'igualdade'
# Representa o sinal de maior que '>'
t_maior_que = 'maior_que'
# Representa o sinal de menor que '<'
t_menor_que = 'menor_que'
# Representa o sinal de maior ou igual '>='
t_maior_igual = 'maior_igual'
# Representa o sinal de menor ou igual '<='
t_menor_igual = 'menor_igual'
# Representa o sinal de diferença '!='
t_diferente = 'diferente'

# Representa a palavra-chave 'se'
t_se = 'se'
# Representa a palavra-chave 'fimse'
t_fim_se = 'fim_se'
# Representa a palavra-chave 'repita'
t_repita = 'repita'
# Representa a palavra-chave 'fimrepita'
t_fim_repita = 'fim_repita'
# Representa a palavra-chave 'func'
t_funcao = 'funcao'
# Representa a palavra-chave 'fimfunc'
t_fim_funcao = 'fim_funcao'
# Representa a palavra-chave 'retorna'
t_retorna = 'retorna'

# Representa a palavra-chave 'inteiro'
t_tipo_inteiro = 'tipo_inteiro'
# Representa a palavra-chave 'flutuante'
t_tipo_flutuante = 'tipo_flutuante'
# Representa a palavra-chave 'texto'
t_tipo_texto = 'tipo_texto'

# Representa a palavra-chave 'escreva'
t_escreva = 'escreva'
# Representa a palavra-chave 'leia'
t_leia = 'leia'

# Representa a palavra-chave 'importa'
t_importa = 'importa'

# Representa um modelo(classe)
t_modelo = 'modelo'