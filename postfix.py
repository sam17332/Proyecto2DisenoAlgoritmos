class Postfix:
    def __init__(self):
        self.precedencia = {'|': 1,'.': 2, '*': 3}  # Diccionario de precedencia
        self.top = -1 # Contador
        self.operadores = ["|", ".", "*", "(", ")"]  # Diccionario operadores
        self.opeArr = [] # Array usado como pila
        self.pstFx = [] # Array donde se van concatenando
        self.concat = '' # String donde se va concatenando

    def vacio(self):
        return True if self.top == -1 else False

    # Funcion para verificar si el caracter es un operador
    def isOperador(self, char):
        if char == '|' or char == '.' or char == '*':
            return True
        return False

    # Se agrega el elemnento
    def push(self, op):
        self.top += 1
        self.opeArr.append(op)

    # Funcion para verificar que el caracter no sea un operador
    def notOperador(self, ope):
        valido=False
        for i in self.operadores:
            if(ope == i):
                valido = False
                break
            else:
                valido = True

        if valido:
            return True

        return False

    # Retorna el valor de hasta arriba de la pila
    def stack(self):
        return self.opeArr[-1]

    # Hace pop de el ultimo elemento de la pila
    def pop(self):
        if not self.vacio():
            self.top -= 1
            return self.opeArr.pop()
        else:
            return "$"

     # Funcion para obtener que caracter tiene mas precedencia
    def masPrecedencia(self, i):
        a = self.precedencia[i]
        b = self.precedencia[self.stack()]

        return True if a <= b else False

     # Funcion para armar el postfix
    def toPostfix(self, exp):
        # Iteramos la exprecion
        for i in exp:
            # Si i es un operador
            if self.isOperador(i):
                if(self.concat != ''):
                    self.pstFx.append(self.concat)
                    self.concat = ''
                while len(self.opeArr) > 0 and self.opeArr[-1] != '(' and self.masPrecedencia(i):
                    top = self.pop()
                    self.pstFx.append(top)
                self.push(i)
            # Si i no es un operador
            elif self.notOperador(i):
                self.concat = self.concat+i
            # Si i es un "("
            elif i == '(':
                self.push(i)
            # Si i es un ")"
            elif i == ')':
                if(self.concat != ''):
                    self.pstFx.append(self.concat)
                    self.concat = ''
                # Mientras no esté vacío y sea diferente a "("
                while((not self.vacio()) and self.stack() != '('):
                    a = self.pop()
                    self.pstFx.append(a)
                    if len(a) == 0:
                        print("No hay signo de cerrado de paréntesis")
                # Si no está vacío y es diferente a "("
                if (not self.vacio() and self.stack() != '('):
                    return -1
                else:
                    self.pop()
            else:
                while(not self.vacio() and self.masPrecedencia(i)):
                    self.pstFx.append(self.pop())
                self.push(i)
        if(self.concat != ''):
            self.pstFx.append(self.concat)

        while len(self.opeArr):
            caracter = self.pop()
            if caracter == "(":
                print("Hace falta un ')'")
            self.pstFx.append(caracter)

        return "".join(self.pstFx)
