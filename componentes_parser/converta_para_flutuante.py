from componentes_parser.no import No

# Esta é uma função interna utilizada para converter uma expressão para o tipo de dado flutuante
class ConvertaParaFlutuante(No):
    def __init__(self, expr: No):
        self._expr = expr

    def retornaExpr(self):
        return self._expr