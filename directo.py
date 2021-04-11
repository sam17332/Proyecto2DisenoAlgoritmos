from graphviz import Digraph
from nodoD import *

class Directo:
    def __init__(self, postfix, cadena):
        self.postfix = postfix
        self.cadena = cadena
        self.lenguaje = []
        self.diccioFinal = {}
        self.diccioSiguientePos = {}
        self.contador1 = 1
        self.contador2 = 0
        self.pila = []
        self.pilaFinal = []
        self.Destados = []
        self.DestadosGlobal = []

    """
    Función para obtener el lenguaje del postfix.
    """
    def getLenguaje(self, postfix):
        lenguaje = ''.join(set(str(postfix)))

        for char in lenguaje:
            if(char.isalnum() or char == 'ɛ'):
                if char not in self.lenguaje:
                    self.lenguaje.append(char)

    """
    Función para obtener los diferentes id's de una letra
    """
    def getIdsLetra(self, letra):
        ids = []
        for id, nodo in self.diccioFinal.items():
            if(nodo.getChar() == letra):
                ids.append(nodo.getId())

        return ids

    """
    Función para saber si el caracter es un operando o un operador.
    Si es un operando, epsilon o numeral, retorna TRUE
    de lo contrario, retorna FALSE
    """
    def esOperando(self, valor):
        if valor.isalnum() or valor == "ɛ" or valor == "#":
            return True
        return False

    """
    Función para saber si el caracter es un anulable o no.
    Si el caracter es:
    ɛ = TRUE
    | = anulable1 or anulable2
    . = anulable1 and anulable2
    * = TRUE
    operando = FALSE
    """
    def esAnulable(self, nodos, char):
        if(char == "ɛ"):
            return True
        elif(self.esOperando(char)):
            return False
        elif (char == "|"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulable1 = nodo1.getAnulable()
            anulable2 = nodo2.getAnulable()

            return (anulable1 or anulable2)
        elif(char == "."):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulable1 = nodo1.getAnulable()
            anulable2 = nodo2.getAnulable()

            return (anulable1 and anulable2)
        elif(char == "*"):
            return True
        else:
            print("ERROR")

    """
    Función para saber la primeraPos de cada caracter
    Si el caracter es:
    ɛ = ø -  vacio
    | = primeraPosC1 U primeraPosC2
    . = anulable(c1) ? primeraPosC1 U primeraPosC2 : primeraPosC1
    * = primeraPosC1
    operando = {id}
    """
    def primeraPos(self, nodos, char):
        if(char == "ɛ"):
            return ""
        elif(self.esOperando(char)):
            nodo1 = nodos.pop()
            nodo1Id = nodo1.getId()

            return [nodo1Id]
        elif (char == "|"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            primeraPos1 = nodo1.getPrimeraPos()
            primeraPos2 = nodo2.getPrimeraPos()

            if(primeraPos1 == ""):
                primeraPos1 = []
            if(primeraPos2 == ""):
                primeraPos2 = []

            arrayLocalOR = primeraPos1+primeraPos2
            arrayLocalOR = list(dict.fromkeys(arrayLocalOR))
            arrayLocalOR.sort()

            return arrayLocalOR
        elif(char == "."):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulable1 = nodo1.getAnulable()
            primeraPos1 = nodo1.getPrimeraPos()
            primeraPos2 = nodo2.getPrimeraPos()

            if(primeraPos1 == ""):
                primeraPos1 = []
            if(primeraPos2 == ""):
                primeraPos2 = []
            if(anulable1):
                arrayLocalCAT = primeraPos1+primeraPos2
            else:
                arrayLocalCAT = primeraPos1

            arrayLocalCAT = list(dict.fromkeys(arrayLocalCAT))
            arrayLocalCAT.sort()

            return arrayLocalCAT
        elif(char == "*"):
            nodo1 = nodos.pop()
            primeraPos1 = nodo1.getPrimeraPos()

            if(primeraPos1 == ""):
                primeraPos1 = []

            arrayLocalKL = primeraPos1
            arrayLocalKL = list(dict.fromkeys(arrayLocalKL))
            arrayLocalKL.sort()

            return arrayLocalKL
        else:
            print("ERROR")

    """
    Función para saber la ultimaPos de cada caracter
    Si el caracter es:
    ɛ = ø  "vacio"
    | = ultimaPosC1 U ultimaPosC2
    . = anulable(c2) ? ultimaPosC1 U ultimaPosC2 : ultimaPosC2
    * = ultimaPosC1
    operando = {id}
    """
    def ultimaPos(self, nodos, char):
        if(char == "ɛ"):
            return ""
        elif(self.esOperando(char)):
            nodo1 = nodos.pop()
            nodo1Id = nodo1.getId()

            return [nodo1Id]
        elif (char == "|"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            ultimaPos1 = nodo1.getUltimaPos()
            ultimaPosC2 = nodo2.getUltimaPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []
            if(ultimaPosC2 == ""):
                ultimaPosC2 = []

            arrayLocalOR = ultimaPos1+ultimaPosC2
            arrayLocalOR = list(dict.fromkeys(arrayLocalOR))
            arrayLocalOR.sort()

            return arrayLocalOR
        elif(char == "."):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulableC2 = nodo2.getAnulable()
            ultimaPos1 = nodo1.getUltimaPos()
            ultimaPosC2 = nodo2.getUltimaPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []
            if(ultimaPosC2 == ""):
                ultimaPosC2 = []
            if(anulableC2):
                arrayLocalCAT = ultimaPos1+ultimaPosC2
            else:
                arrayLocalCAT = ultimaPosC2

            arrayLocalCAT = list(dict.fromkeys(arrayLocalCAT))
            arrayLocalCAT.sort()

            return arrayLocalCAT
        elif(char == "*"):
            nodo1 = nodos.pop()
            ultimaPos1 = nodo1.getUltimaPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []

            arrayLocalKL = ultimaPos1
            arrayLocalKL = list(dict.fromkeys(arrayLocalKL))
            arrayLocalKL.sort()

            return arrayLocalKL

        else:
            print("ERROR")

    """
    Función para saber la siguientePos de cada caracter
    Si el caracter es:
    . = Para cada id que este en ultimaPos de C1, incerte cada id que este en primeraPos de C2
    * = Para cada id que este en primeraPos de C1, incerte cada id que este en ultimaPos de C1
    """
    def siguientePos(self, nodos, char):
        if(char == "."):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            ultimaPos1 = nodo1.getUltimaPos()
            primeraPos2 = nodo2.getPrimeraPos()

            if(primeraPos2 == ""):
                primeraPos2 = []
            if(ultimaPos1 == ""):
                ultimaPos1 = []

            arrayLocal = []
            for x in ultimaPos1:
                arrayLocal = self.diccioSiguientePos[int(x)]
                arrayLocal = arrayLocal+primeraPos2
                arrayLocal = list(dict.fromkeys(arrayLocal))
                arrayLocal.sort()
                self.diccioSiguientePos[int(x)] = arrayLocal

        elif(char == "*"):
            nodo1 = nodos.pop()
            ultimaPos1 = nodo1.getUltimaPos()
            primeraPosC1 = nodo1.getPrimeraPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []
            if(primeraPosC1 == ""):
                primeraPosC1 = []

            for x in ultimaPos1:
                arrayLocal = self.diccioSiguientePos[int(x)]
                arrayLocal = arrayLocal+primeraPosC1
                arrayLocal = list(dict.fromkeys(arrayLocal))
                arrayLocal.sort()
                self.diccioSiguientePos[int(x)] = arrayLocal

        else:
            print("ERROR")

    """
    Función para obtener el id de los estados finales del AFD
    """
    def getFinalNumber(self):
        for id, value in self.diccioSiguientePos.items():
            if len(value) == 0:
                return id
        return ""

    """
    Función para obtener los estados finales del AFD
    """
    def getEstadosFinales(self):
        finales = []
        numeroEstadoFinal = self.getFinalNumber()
        for estado in self.pilaFinal:
            if(str(numeroEstadoFinal) in estado[0]):
                if(estado[0] not in finales):
                    finales.append(estado[0])

        return finales

    """
    Función para graficar el AFD
    """
    # (a|b)*abb
    def graficar(self):
        dig = Digraph()
        dig.attr(rankdir="LR", size="50")
        estadosFinales = self.getEstadosFinales()
        print("estadosFinales")
        print(estadosFinales)
        for nodo in estadosFinales:
            # estadoFinal = estadosFinales.pop()
            posicionDelFinal = self.DestadosGlobal.index(nodo)
            dig.attr("node", shape="doublecircle")
            dig.node(str(posicionDelFinal))
        for nodo in self.pilaFinal:
            if(nodo[1] != 'ɛ' and len(nodo[2]) > 0):
                if(nodo[0] in self.DestadosGlobal and nodo[2] in self.DestadosGlobal):
                    index1 = self.DestadosGlobal.index(nodo[0])
                    index2 = self.DestadosGlobal.index(nodo[2])
                dig.attr("node", shape="circle")
                dig.edge(str(index1), str(index2), nodo[1])

        dig.render("Automatas/Directo.gv", view=True)

    """
    Función para armar el arbol de caracteres.
    Se lee cada caracter y se setea id, anulable, primeraPos
    ultimas y siguientePos para cada nodo dependiendo del caracter
    """
    def arbolDirecto(self):
        self.getLenguaje(self.postfix)
        for char in self.postfix:
            if(char == "|"):
                nodosAnulable = ""
                nodosPrimeraPos = ""
                nodosUltimaPos = ""
                nodo2 = self.pila.pop()
                nodo1 = self.pila.pop()

                nodoOR = NodoD()
                nodoOR.setChar(char)
                nodoOR.setId("")

                nodosAnulable = [nodo2, nodo1]
                nodosPrimeraPos = [nodo2, nodo1]
                nodosUltimaPos = [nodo2, nodo1]

                nodoOR.setAnulable(self.esAnulable(nodosAnulable, char))
                nodoOR.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char))
                nodoOR.setUltimaPos(self.ultimaPos(nodosUltimaPos, char))

                self.diccioFinal[self.contador2] = nodoOR
                self.contador2 += 1
                self.pila.append(nodoOR)

            elif(char == "*"):
                nodosAnulable = ""
                nodosPrimeraPos = ""
                nodosUltimaPos = ""
                nodosSiguientePos = ""
                nodo = self.pila.pop()

                nodoKL = NodoD()
                nodoKL.setChar(char)
                nodoKL.setId("")

                nodosAnulable = [nodo]
                nodosPrimeraPos = [nodo]
                nodosUltimaPos = [nodo]
                nodosSiguientePos = [nodo]

                nodoKL.setAnulable(self.esAnulable(nodosAnulable, char))
                nodoKL.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char))
                nodoKL.setUltimaPos(self.ultimaPos(nodosUltimaPos, char))
                self.siguientePos(nodosSiguientePos, char)

                self.diccioFinal[self.contador2] = nodoKL
                self.contador2 += 1
                self.pila.append(nodoKL)

            elif(char == "."):
                nodosAnulable = ""
                nodosPrimeraPos = ""
                nodosUltimaPos = ""
                nodosSiguientePos = ""
                nodo2 = self.pila.pop()
                nodo1 = self.pila.pop()

                nodoCAT = NodoD()
                nodoCAT.setChar(char)
                nodoCAT.setId("")

                nodosAnulable = [nodo2, nodo1]
                nodosPrimeraPos = [nodo2, nodo1]
                nodosUltimaPos = [nodo2, nodo1]
                nodosSiguientePos = [nodo2, nodo1]

                nodoCAT.setAnulable(self.esAnulable(nodosAnulable, char))
                nodoCAT.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char))
                nodoCAT.setUltimaPos(self.ultimaPos(nodosUltimaPos, char))
                self.siguientePos(nodosSiguientePos, char)

                self.diccioFinal[self.contador2] = nodoCAT
                self.contador2 += 1
                self.pila.append(nodoCAT)

            elif(char == "ɛ"):
                nodos = ""

                nodoEP = NodoD()
                nodoEP.setChar(char)
                nodoEP.setId("")

                nodos = [nodoEP]

                nodoEP.setAnulable(self.esAnulable(nodos, char))
                nodoEP.setPrimeraPos(self.primeraPos(nodos, char))
                nodoEP.setUltimaPos(self.ultimaPos(nodos, char))

                self.diccioFinal[self.contador2] = nodoEP
                self.contador2 += 1
                self.pila.append(nodoEP)

            else:
                nodosAnulable = ""
                nodosPrimeraPos = ""
                nodosUltimaPos = ""

                nodo = NodoD()
                nodo.setChar(char)
                nodo.setId(str(self.contador1))

                self.diccioSiguientePos[self.contador1] = []
                self.contador1 += 1

                nodosAnulable = [nodo]
                nodosPrimeraPos = [nodo]
                nodosUltimaPos = [nodo]

                nodo.setAnulable(self.esAnulable(nodosAnulable, char))
                nodo.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char))
                nodo.setUltimaPos(self.ultimaPos(nodosUltimaPos, char))

                self.diccioFinal[self.contador2] = nodo
                self.contador2 += 1
                self.pila.append(nodo)

        # (a|b)*abb
        nodoRoot = self.pila.pop()
        primerEstado = nodoRoot.getPrimeraPos()
        self.Destados.append(primerEstado)
        self.DestadosGlobal.append(primerEstado)
        while(len(self.Destados) > 0):
            estado = self.Destados.pop()
            for letra in self.lenguaje:
                idsLetra = self.getIdsLetra(letra)
                array = []
                for id in idsLetra:
                    if(id in estado):
                        array = array + self.diccioSiguientePos[int(id)]

                if(array not in self.DestadosGlobal):
                    self.Destados.append(array)
                    self.DestadosGlobal.append(array)
                    self.pilaFinal.append([estado, letra, array])

                else:
                    if(len(estado) > 0):
                        self.pilaFinal.append([estado, letra, array])

        self.graficar()