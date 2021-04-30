<h1 align="center">
<br>
Generador de analizadores léxicos
</h1>

<p align="center">Universidad del Valle de Guatemala</p>
<p align="center">Diseño de Lenguajes de Programación</p>
<p align="center">Proyecto # 2</p>
<p align="center">Rodrigo Samayoa - 17332</p>
<p align="center">29/04/2021</p>

<hr />

## De que trata

<h4>El proyecto consiste en la implementación de un generador de analizadores léxicos, tomando como base un subconjunto de las características de COCOr. El programa aceptará como entrada un archivo en COCOl, con la especificación del analizador léxico a generar, y dará como salida un archivo fuente, el cual implementará el scanner basado en la gramática ingresada.<h4>

# Descripción de herramientas  y archivos archivos

## Listado de herramientas usadas para el proyecto

- Python 3.8.0 64bits
- Visual Studio Code
- Una terminal

## Liberías Necesarias

- Python 3.8.0
  - Una versión de Python igual o mayor a Python 3.6.0 64bits
- pickle
  - Libreria para serializar objetos. [link de documentaciǿn](https://docs.python.org/3/library/pickle.html)
- pprint
  - Libreria para imprimir y mostrar los caracteres especiales
- Terminal
  - Terminal de la computadora o terminal de VS Code

## Archivos y carpetas
1. main.py: Programa principal donde se lee el archivo COCOl y se genera el scanner.py.
2. funciones.py: Programa con funciones auxiliares para poner operar y ordenar los Characters que se leen en main.py.
3. directo.py: Programa donde se genera el AFD con el algoritmo directo.
4. nodoD.py: Clase que contiene las propiedades necesarias que necesita el metodo de directo para poder ser generado.
5. tipoChar.py: Clase con las variables necesarias para poder guardar los caracteres o characters que tiene cada token.
6. postfix.py: Programa que contiene las funciones necesariasmpara pasar a postfix lo tokens leídos en main.py.
7. scanner.py: Programa generado a partir del main.py para obtener los tokens que encuentra en el txt dependiendo de la gramatica ingresada.
8. lectura.txt: archivo de texto para probar al correr el scanner.py
9. Automatas: Carpeta donde se encuentra un pdf, para visualizar el AFD, para cada gramatica.
10. cocols: Carpeta donde se encuentras las diferentes gramaticas que se pueden escoger al ejecutar main.py

## Link Youtube
#### Video que explica todo el programa y las funciones:

## Orden de como correr el proyecto

- Abrir terminal.
    - Ir al path donde este todo el proyecto.
- Ejecutar en la consola el programa `main.py` por medio del comando `python3 main.py`.
    - Al correrlo debe escribr el nombre completo de uno de los archivos ATG que se encuentran en la carpeta "cocols".
    - Esto generara o actualizara 3 diferentes archivos:
        - diccioAceptacion: Contiene un diccionario donde se definen los estados de aceptacion de cada token.
        - pilaFinal: Contiene el AFD.
        - scanner.py: Programa a ejecutar en siguiente paso.
- Luego ejecutar `scanner.py` por medio del comando `python3 scanner.py`.
    - Al correrlo debe escribr el nombre completo del archivo txt de prueba o el txt que desee probar.
    - Esto le imprimira en consola los tokens que encuentre en el txt.
