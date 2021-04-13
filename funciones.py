class Funciones:
    def __init__(self):
        self.top = -1
        self.arrayOperandos = []
        self.outputPostfix = []
        self.precedencia = {'+': 1, '-': 1, }
        self.stack2 = []
        self.top2 = -1
        self.concatenado = ''

    def is_op(self, a):
        if a == '+' or a == '-':
            return True
        return False

    def isEmpty(self):
        return True if self.top == -1 else False

    def peekTopOfStack(self):
        return self.arrayOperandos[-1]

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.arrayOperandos.pop()
        else:
            return "$"

    def pop2(self):
        if self.top2 == -1:
            return
        else:
            self.top2 -= 1
            return self.stack2.pop()

    def push2(self, i):
        self.top2 += 1
        self.stack2.append(i)

    def push(self, op):
        self.top += 1
        self.arrayOperandos.append(op)

    def isOperando(self, ch):
        if ch.isalnum() or ch == "ɛ" or ch == '"' or ch == "'":
            return True
        return False

    def mayorPrecedencia(self, i):
        try:
            a = self.precedencia[i]
            b = self.precedencia[self.peekTopOfStack()]
            return True if a <= b else False
        except KeyError:
            return False

    def infixToPostfix(self, exp):
        exp = exp.replace(" ", "")
        for i in exp:
            if self.isOperando(i):
                self.concatenado = str(self.concatenado+i)
            elif self.is_op(i):
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                while len(self.arrayOperandos) > 0 and self.arrayOperandos[-1] != '(' and self.mayorPrecedencia(i):
                    top = self.pop()
                    self.outputPostfix.append(top)
                self.push(i)
            elif i == '(':
                self.push(i)
            elif i == ')':
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                while((not self.isEmpty()) and self.peekTopOfStack() != '('):
                    a = self.pop()  # hacemos pop
                    self.outputPostfix.append(a)  # agregamos al outputPostfix
                    if len(a) == 0:
                        print("No hay signo de cerrado de paréntesis")
                        return -1
                if (not self.isEmpty() and self.peekTopOfStack() != '('):
                    return -1
                else:
                    self.pop()
            else:
                while(not self.isEmpty() and self.mayorPrecedencia(i)):
                    self.outputPostfix.append(self.pop())
                self.push(i)

        if(self.concatenado != ''):
            self.outputPostfix.append(self.concatenado)

        while len(self.arrayOperandos):
            caracter = self.pop()
            if caracter == "(":
                print("Hay un signo de paréntesis abierto de más")
                exit(-1)
            self.outputPostfix.append(caracter)

        return " ".join(self.outputPostfix)

    def operatePostFix(self, expresion):
        expresion = expresion.replace("'", "")
        expresion = expresion.replace('"', "")
        print("expresion: " + expresion)
        arrayLocal = expresion.split()
        print(arrayLocal)
        for i in arrayLocal:
            resultado = ""
            array = []
            if(self.isOperando(i)):
                for j in i:
                    array.append(str(j))
                self.push2(array)
            else:
                val1 = set(self.pop2())
                val2 = set(self.pop2())

                if(i == "+"):
                    resultado = val1 | val2
                elif(i == "-"):
                    resultado = val2 - val1

                self.push2(resultado)

        operacion = self.pop2()
        cadena = ""
        for i in operacion:
            cadena += i

        return str(cadena)


# Probamos la funcionalidad
# expresion = input('Ingresa una expresión:  ')
# expresion = expresion.replace(' ', '')
# obj = Funciones()
# postFixValue = obj.infixToPostfix(expresion)
# #print(postFixValue)
# strconv = postFixValue.split(' ')
# #print(strconv)
# resultado = obj.operatePostFix(strconv)
# print(f'El resultado es: {resultado}')

