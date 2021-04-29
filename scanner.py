
import pickle5 as pickle
import pprint

class Scanner:
    def __init__(self, documentoALeer):
        self.diccioAceptacion = {}
        self.pilaFinal = []
        self.cadenaALeer = ""
        self.nombreDocALeer = documentoALeer
        self.print = pprint.PrettyPrinter()

    def main(self):
        self.openFiles()

        with open(self.nombreDocALeer, "r") as f:
            self.cadenaALeer = f.read()
        f.close()

        self.simular()

    def openFiles(self):
        file = open("pilaFinal", "rb")
        self.pilaFinal = pickle.load(file)
        file.close()

        file = open("diccioAceptacion", "rb")
        self.diccioAceptacion = pickle.load(file)
        file.close()

    def getStateNumber(self, array):
        for valor in self.pilaFinal:
            if(valor[1] == array):
                return valor[0]

    def mover(self, estados, caracter):
        array = []
        for estado in estados:
            for transicion in self.pilaFinal:
                for i in transicion[2]:
                    if(
                        ord(caracter) == i
                        and len(transicion[3]) > 0
                        and estado == transicion[0]
                    ):
                        estadoSiguiente = self.getStateNumber(transicion[3])
                        if(estadoSiguiente not in array):
                            array.append(estadoSiguiente)

        return array

    def getToken(self, estados):
        token = ""
        for transicion in self.pilaFinal:
            for estado in estados:
                if(estado == transicion[0]):
                    for estadoInd in transicion[1]:
                        for key, valor in self.diccioAceptacion.items():
                            if(int(estadoInd) == int(key)):
                                token = valor

                                return token

        return token

    def simular(self):
        cadena = []
        s = [0]
        s2 = [0]
        cont = 0
        tokenDef = ""
        for i in self.cadenaALeer:
            cadena.append(i)
        cadena.append(" ")

        while len(cadena) > 0:
            # Si no se esta en el ultimo caracter de la cadena
            if(cont == len(self.cadenaALeer)-1):
                char = self.cadenaALeer[cont]
                tokenDef += char
                s = self.mover(s, char)
                token = self.getToken(s)
                if(len(token) == 0):
                    self.print.pprint("La cadena " + str(tokenDef) + " es un token invalido!")
                    break
                self.print.pprint("La cadena " + str(tokenDef) + " es el token " + str(token))
                break

            char1 = self.cadenaALeer[cont]
            char2 = self.cadenaALeer[cont+1]
            tokenDef += char1
            s = self.mover(s, char1)
            s2 = self.mover(s, char2)

            # Si el caracter siguiente no tiene transicion,
            # pero el caracter  actual si
            if(len(s2) == 0 and len(s) > 0):
                token = self.getToken(s)
                # Si se encontro un token
                if(len(token) == 0):
                    self.print.pprint("La cadena " + tokenDef + " es un token invalido!")
                    s = [0]
                    s2 = [0]
                    tokenDef = ""
                    cont -= 1
                else:
                    self.print.pprint("La cadena " + tokenDef + " es el token " + token)
                    s = [0]
                    s2 = [0]
                    tokenDef = ""
            # Si no hay transicion
            elif(len(s) == 0):
                self.print.pprint("La cadena " + tokenDef + " es un token invalido!")
                s = [0]
                s2 = [0]
                tokenDef = ""

            cont += 1
            cadena.pop()

def menu():
    nombre = str(input("Ingrese el nombre del archivo que desea leer: "))

    main = Scanner(nombre)
    main.main()

menu()
            