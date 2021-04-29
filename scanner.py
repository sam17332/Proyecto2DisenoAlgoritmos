import pickle5 as pickle
from pprint import pprint as pp

class Scanner:
    def __init__(self, documentoALeer):
        self.diccioSiguientePos = {}
        self.diccioAceptacion = {}
        self.pilaFinal = []
        self.cadenaALeer = ""
        self.nombreDocALeer = documentoALeer

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

        file = open("diccioSiguientePos", "rb")
        self.diccioSiguientePos = pickle.load(file)
        file.close()

        file = open("diccioAceptacion", "rb")
        self.diccioAceptacion = pickle.load(file)
        file.close()

    def getFinalNumber(self):
        arrayLocal = []
        for id, value in self.diccioSiguientePos.items():
            if len(value) == 0 and id not in arrayLocal:
                arrayLocal.append(id)

        return arrayLocal

    def getEstadosFinales(self):
        finales = []
        numeroEstadoFinal = self.getFinalNumber()
        for estado in self.pilaFinal:
            for estadoFinal in numeroEstadoFinal:
                if(str(estadoFinal) in estado[1] and estado[1] not in finales):
                    finales.append(estado[0])

        return finales

    def getStateNumber(self, array):
        for valor in self.pilaFinal:
            if(valor[1] == array):
                return valor[0]

    """
    Funcion para encontrar el siguiente estado
    """
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
        print(self.diccioAceptacion)
        for transicion in self.pilaFinal:
            for estado in estados:
                print("estado")
                print(estado)
                if(estado == transicion[0]):
                    for estadoInd in transicion[1]:
                        print("estadoInd")
                        print(estadoInd)
                        if(estadoInd in self.diccioAceptacion):
                            token = self.diccioAceptacion[estado]

        return token

    def simular(self):
        cadena = []
        s = [0]
        cont = 0
        for i in self.cadenaALeer:
            cadena.append(i)
        cadena.append(" ")

        while len(cadena) > 0:
            char = self.cadenaALeer[cont]
            print(char)
            sBefore = s
            s = self.mover(s, char)
            print(s)

            if(len(s) == 0):
                token = self.getToken(sBefore)
                if(len(token) == 0):
                    print("Token invalido")
                    s = [0]
                    cont -= 1
                else:
                    print("El token encontrado es" + str(token))
            cont += 1
            cadena.pop()


def menu():
    # nombre = str(input("Ingrese el nombre del archivo que desea leer"))
    nombre = "lectura.txt"

    main = Scanner(nombre)
    main.main()

menu()