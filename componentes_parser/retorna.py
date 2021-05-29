from componentes_parser.no import No

class Retorna(No):
    def __init__(self, expr: No):
        self._expr = expr

    def retornaExpr(self):
        return self._expr