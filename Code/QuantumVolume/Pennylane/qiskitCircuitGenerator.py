from qiskit.circuit.library import QuantumVolume as QV
from qiskit import qasm2
import argparse
import sys

def main(args=None):
    parser = argparse.ArgumentParser(description="Generate a Quantum Volume circuit.")
    parser.add_argument("num_qubits", type=int, help="Number of qubits (must be > 2)")
    parsed_args = parser.parse_args(args)

    if parsed_args.num_qubits <= 2:
        print("Error: num_qubits must be greater than 2.")
        sys.exit(1)

    circuit = QV(num_qubits=parsed_args.num_qubits, depth=parsed_args.num_qubits)
    circuit = circuit.decompose(reps=5)

    circuitoQASM = qasm2.dumps(circuit)
    with open("qv_circuit.qasm", "w") as f:
        print(circuitoQASM)
        f.write(circuitoQASM)

if __name__ == "__main__":
    main()