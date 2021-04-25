class TipoChar:
    def __init__(self):
        self.tipo = ""
        self.valor = ""

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getTipoChar(self):
        return [self.tipo, self.valor]