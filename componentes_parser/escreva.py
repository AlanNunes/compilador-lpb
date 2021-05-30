from componentes_parser.no import No

# Esta é uma função interna utilizada para imprimir texto no console.
class Escreva(No):
    def __init__(self, expr: No):
        self._expr = expr

    def retornaExpr(self):
        return self._expr