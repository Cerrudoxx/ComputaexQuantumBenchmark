###Imports necesarios
import numpy as np
import math
import re


from qiskit import transpile, QuantumCircuit

#-----------------------------------------------
from qiskit.qasm2 import dumps
#-----------------------------------------------

def cod_qasm(qc):
## Descripción: Convierte el circuito de Qiskit a código QASM
## Input: Circuito a estudiar. (Tipo QuantumCircuit)
## Output: Código QASM equivalente. (Tipo string)

    qc_transpilado = transpile(qc, basis_gates=['rx', 'cx', 'x', 'h', 'ry', 'cy', 'y', 'rz', 'cz', 'z'])
    codigo = dumps(qc_transpilado)
    
    return codigo


def crear_archivoqasm(n, codigo_qasm):
## Descripción: Genera el archivo con extensión .qasm a partir de la información introducida. Además, muestra por pantalla un mensaje de éxito si se ha realizado correctamente.
## Input: - Nombre/ruta del archivo que se generará. (Tipo String)
##	  - Código QASM con la información del circuito. (Tipo String)
## Output:

    with open(n, "w") as archivo:
        archivo.write(codigo_qasm)

    print(f"Se ha guardado la cadena en el archivo '{n}'.")



def importar_qasm(n):
## Descripción: Obtiene, a partir de un archivo con extensión .qasm, toda la información del circuito. Es la función inversa a crear_archivoqasm()
## Input: Nombre/ruta del archivo a importat. (Tipo String)
## Output: Circuito importado en código QASM. (Tipo String)

    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read()
    return contenido


def lista_qasm(qasm):
## Descripción: Elimina del código la información que no tenga que ver con las puertas utilizadas. La inicialización la suprime y la información del número de qubits la reserva.
## Input: Código QASM. (Tipo String)
## Output: - Lista con cada línea de código QASM. (Tipo Lista)
##	   - Número de qubits que utiliza el circuito. (Tipo Int)

    lista = qasm.splitlines()
    n = lista[2].split("qreg q[")[1].split("]")[0] #Hacerlo con el re
    
    #Las medidas en qasm2 se expresan en la linea 4, guardaremos el numero de medidas por si hiciera falta y procesamos el resto
    # Extraer el número de medidas de la línea 'meas[<num>];'
    nMeas = int(re.search(r'meas\[(\d+)\]', lista[3]).group(1)) if re.search(r'meas\[(\d+)\]', lista[3]) else None
    print(nMeas)

    lista = lista[4:-(nMeas+1)] if nMeas is not None else lista[4:]
    lista2 = []
    lista2.append(n) #Añadimos el número de qubits al principio de la lista
    for i in lista:
        #print(i)
        j = puerta(i,"psi")
        lista2.append(j)
    
    return lista2,n



def puerta (cadena, registro):
## Descripción: Esta función transforma una línea de código QASM en su equivalente en Intel-QS.
## Input: - Comando de una puerta en QASM en la que se expresan el tipo de puerta y el o los qubits a los que se aplica. (Tipo String)
##        - Nombre del registro cuántico o circuito en Intel-QS. (Tipo String) ###Puede que lo elimine porque siempre utilizo "psi"??
## Output: Equivalencia en Intel-QS del comando (puerta) introducido en QASM. (Tipo String)
    
    palabras = cadena.split()
    # print("palabras:", palabras)

    partes = palabras[0].split("(")
    # print("partes:", partes)

    if (len(palabras[0]) > 2):
        
        angulo = partes[1].replace("pi", "M_PI")
        qubits = re.findall(r'\[(.*?)\]', palabras[1])
        qubits= qubits[0]
        apply = (registro+".ApplyRotation"+partes[0][1].upper()+"("+qubits+", "+angulo+";")
    else:
        if (len(palabras[0])==2):
            
            qubits = re.findall(r'q\[(\d+)\]', palabras[1])
            qubits = ",".join(qubits)

            apply = (registro+".ApplyCPauli" + palabras[0][1].upper()+"("+qubits+");")
        
        if (len(palabras[0])==1):
            qubits = re.findall(r'\[(.*?)\]', palabras[1])
            qubits= qubits[0]
            if (palabras[0]!="h"):
                apply = (registro+".ApplyPauli" + palabras[0].upper()+"("+ str(qubits) +");")
            else:
                apply = registro+".ApplyHadamard"+"("+qubits+");"
    

    return apply


def inicioqasm():
## Descripción: Función interna del programa (el usuario no la utilizará explícitamente). Se encarga de inicializar el archivo a partir de otro contenido en el directorio de trabajo llamado "inicio.qasm".
## Input: -
## Output: Líneas de código necesarias para el funcionamiento de la librería. (Tipo Lista)

    with open("inicio.qasm", "r") as archivo:
        inicio = archivo.read()
    return inicio


def fin_qasm():
## Descripción: Función interna del programa (el usuario no la utilizará explícitamente). Se encarga de añadir al final del código QASM la información necesaria para su correcto funcionamiento.
## Input: -
## Output: Línea de código necesaria para el funcionamiento de la librería. (Tipo String)       
    with open("finConQubits.qasm", "r") as archivo:
        fin = archivo.read()
    return fin


def crearcpp(nombrecpp, lista):
## Descripción: Esta función genera el código final con extensión .cpp que podrá ser compilado y ejecutado. El código incluye la información necesaria para inicializar la librería Intel-QS y el circuito a  estudiar.
## Input: - Nombre/ruta del archivo a generar. (Tipo String)
##        - Puertas del circuito expresadas como comandos de Intel-QS. (Tipo Lista)
## Output: - 
    # Escribir el contenido de inicioqasm()
    cpp = inicioqasm()
    # COMENTANDO PARA QUE FUNCIONE CON EL SCRIPT DE GROVER, DESCOMENTAR PARA USARLO INDEPENDIENTEMENTE
    # Escribir cada línea de lista en una línea separada
    for linea in lista[1:]:
        cpp += str(linea) + "\n"

    # Escribir el contenido de fin_qasm()
    cpp += fin_qasm()
        
    with open(nombrecpp, "w") as archivo:
        archivo.write(cpp)

    print(f"Se ha guardado la cadena en el archivo '{nombrecpp}'.")
    
def trad_from_qasm(codigo_qasm, nombrecpp = "qasm.cpp"):
## Descripción: Crea el archivo .cpp a partir del código QASM introducido
## Input: - Código QASM. (Tipo String)
## Output: - 

    lista = lista_qasm(codigo_qasm)
    crearcpp(nombrecpp, lista)
    
def trad_from_qiskit(circuito_qiskit, nombrecpp = "qasm.cpp"):
## Descripción: Crea el archivo .cpp a partir del circuito introducido
## Input: - Circuito Qiskit. (Tipo QuantumCircuit)
## Output: - 
   
    qasm = cod_qasm(circuito_qiskit)
    trad_from_qasm(qasm, nombrecpp)