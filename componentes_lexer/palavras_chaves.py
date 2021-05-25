# Representa a palavra-chave 'se'
se = 'se'
# Representa a palavra-chave 'senão'
senao = 'senão'
# Representa a palavra-chave 'então'
entao = 'então'
# Representa a palavra-chave 'fimse'
fim_se = 'fimse'
# Representa a palavra-chave 'repita'
repita = 'repita'
# Representa a palavra-chave 'fimrepita'
fim_repita = 'fimrepita'
# Representa a palavra-chave 'func'
funcao = 'func'
# Representa a palavra-chave 'fimfunc'
fim_funcao = 'fimfunc'
# Representa a palavra-chave 'retorna'
retorna = 'retorna'

# Representa a palavra-chave 'inteiro'
tipo_inteiro = 'inteiro'
# Representa a palavra-chave 'flutuante'
tipo_flutuante = 'flutuante'
# Representa a palavra-chave 'texto'
tipo_texto = 'texto'

# Representa a palavra-chave 'escreva'
escreva = 'escreva'
# Representa a palavra-chave 'leia'
leia = 'leia'

# Representa a palavra-chave 'importa'
importa = 'importa'

# Representa um modelo(classe)
modelo = 'modelo'

todas = [tipo_inteiro, tipo_flutuante, tipo_texto, se, entao, senao, fim_se, repita, fim_repita, funcao, fim_funcao, retorna, escreva, leia, importa, modelo]
todos_tipos_decl_var = [tipo_inteiro, tipo_flutuante, tipo_texto]

# Retorna a palavra chave de acordo com o nome dela
def retornaPalavraChave(valor):
    i = todas.index(valor)
    p_chave = todas[i]
    return p_chave