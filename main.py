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
        self.funciones = Funciones()

    def main(self):
        pp = pprint.PrettyPrinter()
        self.lectura()

        self.construccionTokens()
        pp.pprint(self.json)

    def lectura(self):
        char = False
        key = False
        tokens = False
        archivo = open(self.nombreArchivo, "r")
        contador = 1
        for linea in archivo.readlines():
            linea = linea.replace("\n", "")
            linea = linea.replace(" ", "")
            if(linea[0:8] == "COMPILER"):
                nombre = linea[9:len(linea)]
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
                arrayChar = linea.split("=")
                if(len(arrayChar) >1):
                    diccionarioChar = self.json["CHARACTERS"]
                    resultado = arrayChar[1]
                    var = str(arrayChar[0].replace(" ", ""))
                    self.characters.append(str(var))
                    stringChar = ""
                    local = ""
                    for char in resultado:
                        stringChar += char
                        if(stringChar in self.characters):
                            stringChar = stringChar.replace(stringChar, diccionarioChar[stringChar])

                    largo = len(stringChar)
                    local = str(stringChar)
                    if(stringChar[largo-1] == "."):
                        local = str(stringChar[0:largo-1])

                    if("+" in local or "-" in local):
                        print(var + ": " + local)
                        local = self.funciones.infixToPostfix(local)
                        local = self.funciones.operatePostFix(local)

                    diccionarioChar[var] = local

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
            definicion = diccionarioToken[key]
            keyInterno = ""
            for char in definicion:
                if(char != " "):
                    keyInterno += char
                    if(str(keyInterno) in self.characters):
                        valor = diccionarioCharacters[keyInterno]
                        array.append(valor)
                        keyInterno = ""
                    elif(char == '"' and esString2 == False):
                        keyInterno = ""
                        if(esString1 == True):
                            esString1 = False
                            array.append("FIN-STRING")
                        else:
                            array.append("STRING")
                            esString1 = True
                    elif(char == "'" and esString1 == False):
                        keyInterno = ""
                        if(esString2 == True):
                            esString2 = False
                            array.append("FIN-CHAR")
                        else:
                            array.append("CHAR")
                            esString2 = True
                    elif(esString1 or esString2):
                        keyInterno = ""
                        array.append(char)
                    elif(char == "{"):
                        array.append("KLEENE")
                        keyInterno = ""
                    elif(char == "}"):
                        array.append("FIN-KLEENE")
                        keyInterno = ""
                    elif(char == "("):
                        array.append("PARENTECIS")
                        keyInterno = ""
                    elif(char == ")"):
                        array.append("FIN-PARENTECIS")
                        keyInterno = ""
                    elif(char == "["):
                        array.append("UNARIO")
                        keyInterno = ""
                    elif(char == "]"):
                        array.append("FIN-UNARIO")
                        keyInterno = ""
                    elif(char == "|"):
                        array.append("OR")
                        keyInterno = ""
            diccionarioToken[key] = array

def menu():
    # print("Ingrese el nombre del archivo que desea leer")
    # nombre = str(input())
    nombre = "cocol4.cfg"

    main = Main(nombre)
    main.main()



menu()









