# Proyecto 2 - Diseño de lenguajes
# Rodrigo Samayoa Morales - 17332
# source proyecto2/bin/activate

import pprint
from funciones import *
from tipoChar import *
from postfix import *
from directo import *

class Main:
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo
        self.json = {}
        self.characters = []
        self.print = pprint.PrettyPrinter()

    def main(self):
        self.lectura()
        # print("chr(39) " + str(chr(39)))
        # print("chr(47) " + str(chr(47)))
        # print("chr(67) " + str(chr(67)))
        # print("chr(72) " + str(chr(72)))
        # print("chr(82) " + str(chr(82)))
        # print("chr(41) " + str(chr(41)))
        # print("chr(40) " + str(chr(40)))
        # print("chr(46) " + str(chr(46)))

        diccionarioCHR = self.json["CHARACTERS"]
        for char in self.characters:
            valor = diccionarioCHR[char]

            if(isinstance(valor, str)):
                funciones = Funciones()
                valor = funciones.getStringInQuotes(valor)
                if(valor[0] == "{" and valor[len(valor)-1] == "}"):
                    if("{" not in valor[1:len(valor)-1]):
                        valor = valor.replace("{", "")

                    if("}" not in valor[0:len(valor)-2]):
                        valor = valor.replace("}", "")
                valor = set(valor)
                diccionarioCHR[char] = valor

        self.construccionTokens()

        # self.print.pprint(self.json)
        # print(self.json)

        tokensLen = len(self.json["TOKENS"])

        # Se crea un array con todos los tokens
        arrayAcumuladoTokens = []
        cont = 0
        for key1, definicion in self.json["TOKENS"].items():
            cont += 1
            for key2, valor in definicion.items():
                arrayAcumuladoTokens.append(valor)
            if(cont < tokensLen):
                tipoChar = TipoChar()
                tipoChar.setTipo("OR")
                tipoChar.setValor(ord("|"))
                arrayAcumuladoTokens.append(tipoChar)

        postfixInst = Postfix()
        postfix = postfixInst.toPostfix(arrayAcumuladoTokens)
        cont = 0
        # for token in postfix:
        #     print(cont)
        #     print(token.getTipoChar())
        #     print(type(token.getValor()))
        #     print()
        #     cont +=1
        # print()

        directoInst = Directo(postfix)
        directoInst.arbolDirecto()



    def lectura(self):
        char = False
        key = False
        tokens = False
        path = str("cocols/" + self.nombreArchivo)
        archivo = open(path, "r+")
        contador = 1
        for linea in archivo.readlines():
            linea = linea.replace("\n", "")
            # linea = linea.replace(" ", "")
            if(linea[0:8] == "COMPILER"):
                nombre = linea[8:len(linea)]
                self.json[linea[0:8]] = nombre
            elif(linea[0:10] == "IGNORECASE"):
                self.json[linea[0:10]] = {}
                char = False
                key = False
                tokens = False
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
                    key = str(arrayChar[0].replace(" ", ""))
                    self.characters.append(str(key))
                    if(resultado[len(resultado)-1] == "."):
                        resultado = resultado[0:len(resultado)-1]

                    funciones = Funciones()
                    # Mandar a ordenar independientemente si hay un + o - en la linea
                    resultado = funciones.infixToPostfix(resultado)

                    # Se itera en los characters que ya existen
                    for character in self.characters:
                        # Si es character esta en la linea se sustituye
                        if(character in resultado):
                            if(isinstance(diccionarioChar[character], set)):
                                stringOfSet = ""
                                for char in diccionarioChar[character]:
                                    stringOfSet += char
                                resultado = resultado.replace(character, str(stringOfSet))
                            elif(isinstance(diccionarioChar[character], str)):
                                resultado = resultado.replace(character, diccionarioChar[character])

                    # Si tiene ANY
                    if('ANY' in resultado):
                        strChars = ""
                        for char in range(0, 256):
                            strChars += chr(char)
                        # setChars = str(set(chr(char) for char in range (0, 255)))
                        # setChars = setChars.replace(" ", "")
                        resultado = resultado.replace("ANY", strChars)

                    # Si hay un CHR
                    if("CHR(" in resultado):
                        funciones = Funciones()
                        # verificar si hay + o - y sustituir CHR
                        if("+" in resultado or "-" in resultado):
                            resultado = self.obtenerCHR(resultado)
                            resultado = funciones.operatePostFix(resultado)
                        else:
                            resultado = self.obtenerCHR(resultado)

                    # Si tiene + o -
                    elif("+" in resultado or "-" in resultado):
                        funciones = Funciones()
                        resultado = funciones.operatePostFix(resultado)

                    # Si tiene ..
                    if(".." in resultado):
                        resultado = self.obtenerRangoLetras(resultado)

                    diccionarioChar[key] = resultado

            elif(key):
                arrayKey = linea.split("=")
                if(len(arrayKey) >1):
                    diccionarioKey = self.json["KEYWORDS"]
                    resultado = arrayKey[1]
                    var = str(arrayKey[0].replace(" ", ""))
                    diccionarioKey[var] = str(resultado)

            elif(tokens):
                linea = linea.replace(" ", "")
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

    def obtenerRangoLetras(self, linea):
        arrayLinea = linea.split("..")
        nuevaLinea = ""
        arrayIntegers = []
        for letra in arrayLinea:
            for char in letra:
                if(char.isalpha()):
                    arrayIntegers.append(ord(char))
                    break

        for char in range(arrayIntegers[0], arrayIntegers[1]+1):
            nuevaLinea += chr(char)

        return nuevaLinea

    def obtenerCHR(self, linea):
        arrayLinea = linea.split(" ")
        arrayPuntos = []
        # arrayCHR = []
        # nuevaLinea = ""
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
                    setChars = str(set(chr(char) for char in range (int(val1), int(val2))))
                    setChars = setChars.replace(" ", "")
                    sustituto = "CHR(" + str(val1) + ")" + " .. " + "CHR(" + str(val2) + ")"
                    linea = linea.replace(sustituto, setChars)
        # else:
        #     for pos in arrayLinea:
        #         if("CHR(" in pos):
        #             arrayCHR.append(i)
        #         i += 1
        #     for i in arrayCHR:
        #         if("CHR(" in arrayLinea[i]):
        #             val1 = arrayLinea[i].replace("CHR(", "")
        #             val1 = val1.replace(")", "")
        #             setChars = str(chr(int(val1)))
        #             setChars = setChars.replace(" ", "")
        #             sustituto = "CHR(" + str(val1) + ")"
        #             nuevaLinea = linea.replace(sustituto, setChars)

        while "CHR(" in linea:
            if("CHR(" in linea):
                pos1 = linea.find("CHR(")
                subStr = linea[pos1:len(linea)]
                pos2 = subStr.find(")")
                val1 = int(subStr[4:pos2])
                strChar = chr(val1)
                sustituto = "CHR(" + str(val1) + ")"
                linea = linea.replace(sustituto, strChar)

        return linea

    def defMultiLinea(self, numeroLinea):
        path = str("cocols/" + self.nombreArchivo)
        archivo = open(path, "r")
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

    def leerString(self, expresion, diccionario, contador):
        posiAct = 0
        tamanio = len(expresion)
        for char in expresion:
            tipoChar = TipoChar()
            tipoChar.setTipo("STRING")
            valor = {ord(char)}
            tipoChar.setCharacter(valor)
            tipoChar.setValor(ord(char))
            diccionario[contador] = tipoChar
            contador += 1
            if(posiAct != tamanio-1):
                tipoChar = TipoChar()
                tipoChar.setTipo("APPEND")
                tipoChar.setValor(ord("."))
                diccionario[contador] = tipoChar
                contador += 1
            posiAct += 1

        return diccionario, contador

    def construccionTokens(self):
        diccionarioToken = self.json["TOKENS"]
        diccionarioCharacters = self.json["CHARACTERS"]
        esString1 = False
        esString2 = False
        for key in diccionarioToken:
            definicion = diccionarioToken[key]
            keyInterno = ""
            cont = 0
            posicionActual = 0
            nuevoDiccionarioToken = {}
            stringConcat = ""
            finalLinea = 0

            tipoChar = TipoChar()
            tipoChar.setTipo("PARENTESIS_INICIAL")
            tipoChar.setValor(ord("("))
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1

            if("EXCEPTKEYWORDS" in definicion.upper()):
                finalLinea = definicion.upper().find("EXCEPTKEYWORDS")

            for char in definicion:
                if(char != " "):
                    keyInterno += char
                    if(str(keyInterno) in self.characters):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("CHARACTER")
                        setChar = diccionarioCharacters[keyInterno]
                        if(isinstance(diccionarioCharacters[keyInterno], set)):
                            setChar = set(ord(str(char)) for char in diccionarioCharacters[keyInterno])
                        tipoChar.setValor(setChar)
                        tipoChar.setCharacter(keyInterno)
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "}"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "]"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                    elif(char == '"' and esString2 == False):
                        keyInterno = ""
                        if(esString1 == True):
                            nuevoDiccionarioToken, cont = self.leerString(stringConcat, nuevoDiccionarioToken, cont)
                            if(posicionActual != len(definicion)-1
                                and definicion[posicionActual+1] != "."
                                and definicion[posicionActual+1] != "|"
                                and definicion[posicionActual+1] != "]"
                                and definicion[posicionActual+1] != "}"
                                and definicion[posicionActual+1] != ")"
                                and (posicionActual+1 < finalLinea
                                or finalLinea == 0)
                            ):
                                tipoChar = TipoChar()
                                tipoChar.setTipo("APPEND")
                                tipoChar.setValor(ord("."))
                                nuevoDiccionarioToken[cont] = tipoChar
                                cont += 1
                            stringConcat = ""
                            esString1 = False
                        else:
                            esString1 = True
                    elif(char == "'" and esString1 == False):
                        keyInterno = ""
                        if(esString2 == True):
                            nuevoDiccionarioToken, cont = self.leerString(stringConcat, nuevoDiccionarioToken, cont)
                            if(posicionActual != len(definicion)-1
                                and definicion[posicionActual+1] != "."
                                and definicion[posicionActual+1] != "|"
                                and definicion[posicionActual+1] != "]"
                                and definicion[posicionActual+1] != "}"
                                and definicion[posicionActual+1] != ")"
                                and (posicionActual+1 < finalLinea
                                or finalLinea == 0)
                            ):
                                tipoChar = TipoChar()
                                tipoChar.setTipo("APPEND")
                                tipoChar.setValor(ord("."))
                                nuevoDiccionarioToken[cont] = tipoChar
                                cont += 1
                            stringConcat = ""
                            esString2 = False
                        else:
                            esString2 = True
                    elif(esString1 or esString2):
                        keyInterno = ""
                        stringConcat += char
                    elif(char == "{"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_INICIAL")
                        tipoChar.setValor(ord("("))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                    elif(char == "}"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_FINAL")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        tipoChar = TipoChar()
                        tipoChar.setTipo("KLEENE")
                        tipoChar.setValor(ord(")"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "]"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "}"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                        keyInterno = ""
                    elif(char == "("):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_INICIAL")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                    elif(char == ")"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_FINAL")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "]"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "}"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                        keyInterno = ""
                    elif(char == "["):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_INICIAL")
                        tipoChar.setValor(ord("("))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                    elif(char == "]"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("OR")
                        tipoChar.setValor(ord("|"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        tipoChar = TipoChar()
                        tipoChar.setTipo("EPSILON")
                        valor = {ord("ɛ")}
                        tipoChar.setCharacter(valor)
                        # tipoChar.setCharacter(set(str(ord("ɛ"))))
                        tipoChar.setValor(ord("ɛ"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_FINAL")
                        tipoChar.setValor(ord(")"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "]"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "}"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                        keyInterno = ""
                    elif(char == "|"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("OR")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                posicionActual += 1
            tipoChar = TipoChar()
            tipoChar.setTipo("APPEND")
            tipoChar.setValor(ord("."))
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1
            tipoChar = TipoChar()
            tipoChar.setTipo("ACEP")
            tipoChar.setCharacter(key)
            tipoChar.setValor(ord("#"))
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1
            tipoChar = TipoChar()
            tipoChar.setTipo("PARENTESIS_FINAL")
            tipoChar.setValor(ord(")"))
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1
            diccionarioToken[key] = nuevoDiccionarioToken
            # print(key)
            # for id, tipo in nuevoDiccionarioToken.items():
            #     print(id)
            #     print(tipo.getTipoChar())
            #     print(type(tipo.getValor()))
            # print()
            # print()
        # print(diccionarioToken)


def menu():
    # nombre = str(input("Ingrese el nombre del archivo que desea leer"))
    # nombre = "HexNumber.ATG"
    # nombre = "Aritmetica.ATG"
    nombre = "CoCoL.ATG"
    # nombre = "Double.ATG"
    # nombre = "cocol2.cfg"

    main = Main(nombre)
    main.main()

menu()