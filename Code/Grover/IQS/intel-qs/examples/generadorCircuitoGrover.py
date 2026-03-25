from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import MCXGate
import math
from datetime import datetime
import funciones_traductor
import sys

# Obtener n como parámetro de entrada
if len(sys.argv) > 1:
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: El parámetro debe ser un número entero.")
        sys.exit(1)
else:
    print("Uso: python generadorCircuitoGrover.py <num_qubits>")
    sys.exit(1)

qc = QuantumCircuit(n)
optimal_num_iterations = math.floor(math.pi / (4 * math.asin(math.sqrt(1 / 2**n))))

# Inicialización
for i in range(n):
    qc.h(i)

# Iteraciones de Grover (oráculo + difusor)
for _ in range(optimal_num_iterations):
    # Oráculo
    qc.h(n - 1)
    qc.append(MCXGate(num_ctrl_qubits=n - 1), range(n))
    qc.h(n - 1)
    # Difusor
    for i in range(n):
        qc.h(i)
        qc.x(i)
    qc.h(n - 1)
    qc.append(MCXGate(num_ctrl_qubits=n - 1), range(n))
    qc.h(n - 1)
    for i in range(n):
        qc.x(i)
        qc.h(i)

input_file = "fin.qasm"
output_file = "finConQubits.qasm"

try:
    # Leer el contenido del archivo de entrada
    with open(input_file, 'r') as file:
        code = file.read()

    # Reemplazar &NUM_QUBITS& por el valor de n
    modified_code = code.replace('&NUM_QUBITS&', str(n))

    # Escribir el código modificado en el archivo de salida
    with open(output_file, 'w') as file:
        file.write(modified_code)

    #print(f"Archivo {output_file} generado exitosamente con el contenido modificado.")

except FileNotFoundError:
    print(f"Error: El archivo {input_file} no se encontró.")
except Exception as e:
    print(f"Error: {e}")

# Medición
qc.measure_all()

codigo_qasm = funciones_traductor.cod_qasm(qc)
#print(codigo_qasm)
funciones_traductor.crear_archivoqasm("circuito2.qasm", codigo_qasm)

lineas, nQubits = funciones_traductor.lista_qasm(codigo_qasm)
#print(lineas)
#print(f"El circuito tiene {nQubits} qubits.")

funciones_traductor.crearcpp("circuito.cpp", lineas)