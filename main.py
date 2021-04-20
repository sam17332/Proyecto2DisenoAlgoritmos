# Proyecto 2 - Diseño de lenguajes
# Rodrigo Samayoa Morales - 17332
# source proyecto2/bin/activate

import pprint
from funciones import *

class Main:
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo
        self.json = {}
        self.characters = []

    def main(self):
        pp = pprint.PrettyPrinter()
        self.lectura()

        self.sustituirOperarCharacters()

        # self.construccionTokens()
        # pp.pprint(self.json)
        print(self.json)

    def lectura(self):
        char = False
        key = False
        tokens = False
        archivo = open(self.nombreArchivo, "r+")
        contador = 1
        for linea in archivo.readlines():
            linea = linea.replace("\n", "")
            # linea = linea.replace(" ", "")
            if(linea[0:8] == "COMPILER"):
                nombre = linea[8:len(linea)]
                self.json[linea[0:8]] = nombre
            elif(linea[0:10] == "CHARACTERS"):
                self.json[linea[0:10]] = {}
                char = True
                key = False
                tokens = False
            elif(linea[0:8] == "KEYWORDS"):
                self.json[linea[0:8]] = {}
                char = False
                key = True
                tokens = False
            elif(linea[0:6] == "TOKENS"):
                self.json[linea[0:6]] = {}
                char = False
                key = False
                tokens = True
            elif(linea[0:11] == "PRODUCTIONS"):
                self.json[linea[0:11]] = {}
                char = False
                key = False
                tokens = False
            elif(linea[0:7] == "PRAGMAS"):
                self.json[linea[0:7]] = {}
                char = False
                key = False
                tokens = False

            if(char):
                arrayChar = linea.split(" = ")
                if(len(arrayChar) >1):
                    diccionarioChar = self.json["CHARACTERS"]
                    resultado = arrayChar[1]
                    var = str(arrayChar[0].replace(" ", ""))
                    self.characters.append(str(var))
                    if(resultado[len(resultado)-1] == "."):
                        resultado = resultado[0:len(resultado)-1]

                    # if("CHR(" in resultado):
                        # resultadoTemp = resultado.replace(" ", "")
                        # resultado = self.obtenerCHR(resultado)

                    diccionarioChar[var] = resultado

                    # resultado = resultado.replace(" ", "")
                    # resString = ""
                    # resTotal = ""
                    # esString = False
                    # for char in resultado:
                    #     if(char != " "):
                    #         if(esString):
                    #             if(char != '"' and char != "'"):
                    #                 resString += char
                    #         else:
                    #             if(char != '"' and char != "'"):
                    #                 resTotal += char

                    #         if(char == '"' or char == "'"):
                    #             if(esString):
                    #                 esString = False
                    #                 resString = set(resString)
                    #                 resTotal += str(resString)
                    #             else:
                    #                 esString = True
                    # print(var)
                    # print(resTotal)
                    # diccionarioChar[var] = resTotal

            elif(key):
                arrayKey = linea.split("=")
                if(len(arrayKey) >1):
                    diccionarioKey = self.json["KEYWORDS"]
                    resultado = arrayKey[1]
                    var = str(arrayKey[0].replace(" ", ""))
                    diccionarioKey[var] = str(resultado)

            elif(tokens):
                arrayToken = linea.split("=")
                if(len(arrayToken) >1):
                    diccionarioToken = self.json["TOKENS"]
                    var = str(arrayToken[0].replace(" ", ""))
                    resultado = arrayToken[1]
                    if(resultado[len(resultado)-1] != "."):
                        resultado = self.defMultiLinea(contador)
                        diccionarioToken[var] = str(resultado)
                    else:
                        diccionarioToken[var] = str(resultado)
            contador += 1

        archivo.close()

    def obtenerCHR(self, linea):
        arrayLinea = linea.split(" ")
        arrayPuntos = []
        arrayCHR = []
        nuevaLinea = ""
        lastVal = 0
        i = 0
        if(".." in arrayLinea):
            for pos in arrayLinea:
                if(".." in pos):
                    arrayPuntos.append(i)
                i += 1

            for i in arrayPuntos:
                if("CHR(" in arrayLinea[i-1] and "CHR(" in arrayLinea[i+1]):
                    val1 = arrayLinea[i-1].replace("CHR(", "")
                    val1 = val1.replace(")", "")
                    val2 = arrayLinea[i+1].replace("CHR(", "")
                    val2 = val2.replace(")", "")
                    lastVal = i+1
                    setChars = str(set(chr(char) for char in range (int(val1), int(val2))))
                    nuevaLinea += setChars
            for i in range(lastVal+1, len(arrayLinea)):
                nuevaLinea += arrayLinea[i]
            # print(nuevaLinea)
        elif("CHR(" in arrayLinea):
            for pos in arrayLinea:
                if("CHR(" in pos):
                    arrayCHR.append(i)
                i += 1
            for i in arrayCHR:
                if("CHR(" in arrayLinea[i]):
                    val1 = arrayLinea[i-1].replace("CHR(", "")
                    val1 = val1.replace(")", "")
                    setChars = str(set(chr(val1)))
                    nuevaLinea += setChars


        return nuevaLinea

    def sustituirOperarCharacters(self):
        diccioChar = self.json["CHARACTERS"]
        for character in self.characters:
            for key in diccioChar:
                definicion = diccioChar[key]
                if(character in definicion):
                    # definicion = set(definicion.replace(character, diccioChar[character]))
                    definicion = definicion.replace(character, diccioChar[character])
                    diccioChar[key] = str(definicion)

        # for key in diccioChar:
        #     definicion = diccioChar[key]
        #     # if("ANY" in definicion):
        #     #     diccioChar[key] = definicion.replace("ANY", str(set(chr(char) for char in range (0, 255))))

        #     nuevaDefinicion = ""
        #     if("+" in definicion or "-"in definicion and "CHR" not in definicion):
        #         funciones = Funciones()
        #         nuevaDefinicion = funciones.infixToPostfix(definicion)
        #         nuevaDefinicion = funciones.operatePostFix(nuevaDefinicion)
        #         diccioChar[key] = nuevaDefinicion

            # print(character)
            # definicion = diccioChar[character]
            # print(definicion)
            # if(character in definicion):
            #     print(definicion)
            #     print()

    def defMultiLinea(self, numeroLinea):
        archivo = open(self.nombreArchivo, "r")
        contador = 1
        resultadoToken = ""
        multiLinea = False
        for linea in archivo.readlines():
            linea = linea.replace(" ", "")
            linea = linea.replace("\n", "")
            if(multiLinea):
                if(linea[len(linea)-1] != "."):
                    resultadoToken += linea
                else:
                    resultadoToken += linea
                    break

            if(multiLinea == False and contador == numeroLinea and linea[len(linea)-1] != "."):
                array = linea.split("=")
                resultadoToken += array[1]
                multiLinea = True

            contador += 1

        archivo.close()

        return resultadoToken


    def construccionTokens(self):
        diccionarioToken = self.json["TOKENS"]
        diccionarioCharacters = self.json["CHARACTERS"]
        esString1 = False
        esString2 = False
        for key in diccionarioToken:
            array = []
            definicionFinal = ""
            definicion = diccionarioToken[key]
            keyInterno = ""
            for char in definicion:
                if(char != " "):
                    keyInterno += char
                    # if(str(keyInterno) in self.characters):
                    #     valor = diccionarioCharacters[keyInterno]
                    #     array.append(valor)
                    #     keyInterno = ""
                    # elif(char == '"' and esString2 == False):
                    #     keyInterno = ""
                    #     if(esString1 == True):
                    #         esString1 = False
                    #         array.append("FIN-STRING")
                    #     else:
                    #         array.append("STRING")
                    #         esString1 = True
                    # elif(char == "'" and esString1 == False):
                    #     keyInterno = ""
                    #     if(esString2 == True):
                    #         esString2 = False
                    #         array.append("FIN-CHAR")
                    #     else:
                    #         array.append("CHAR")
                    #         esString2 = True
                    # elif(esString1 or esString2):
                    #     keyInterno = ""
                    #     array.append('"' + char + '"')
                    # elif(char == "{"):
                    #     array.append('KLEENE')
                    #     keyInterno = ""
                    # elif(char == "}"):
                    #     array.append("FIN-KLEENE")
                    #     keyInterno = ""
                    # elif(char == "("):
                    #     array.append("PARENTECIS")
                    #     keyInterno = ""
                    # elif(char == ")"):
                    #     array.append("FIN-PARENTECIS")
                    #     keyInterno = ""
                    # elif(char == "["):
                    #     array.append("UNARIO")
                    #     keyInterno = ""
                    # elif(char == "]"):
                    #     array.append("FIN-UNARIO")
                    #     keyInterno = ""
                    # elif(char == "|"):
                    #     array.append("OR")
                    #     keyInterno = ""

                    if(str(keyInterno) in self.characters):
                        valor = diccionarioCharacters[keyInterno]
                        definicionFinal += valor
                        keyInterno = ""
                    elif(char == '"' and esString2 == False):
                        keyInterno = ""
                        if(esString1 == True):
                            esString1 = False
                            # definicionFinal += "FIN-STRING "
                        else:
                            # definicionFinal += "STRING "
                            esString1 = True
                    elif(char == "'" and esString1 == False):
                        keyInterno = ""
                        if(esString2 == True):
                            esString2 = False
                            # definicionFinal += "FIN-CHAR "
                        else:
                            # definicionFinal += "CHAR "
                            esString2 = True
                    elif(esString1 or esString2):
                        keyInterno = ""
                        definicionFinal += "'" + char + "'"
                    elif(char == "{"):
                        definicionFinal += "("
                        keyInterno = ""
                    elif(char == "}"):
                        definicionFinal += ")*"
                        keyInterno = ""
                    elif(char == "("):
                        definicionFinal += "("
                        keyInterno = ""
                    elif(char == ")"):
                        definicionFinal += ")"
                        keyInterno = ""
                    elif(char == "["):
                        definicionFinal += "("
                        keyInterno = ""
                    elif(char == "]"):
                        definicionFinal += ")?"
                        keyInterno = ""
                    elif(char == "|"):
                        definicionFinal += "|"
                        keyInterno = ""
            # diccionarioToken[key] = array
            diccionarioToken[key] = definicionFinal

def menu():
    # print("Ingrese el nombre del archivo que desea leer")
    # nombre = str(input())
    nombre = "cocol3.cfg"

    main = Main(nombre)
    main.main()



menu()









