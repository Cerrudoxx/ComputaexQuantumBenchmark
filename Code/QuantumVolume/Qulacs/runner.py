import psutil
from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import Z, H, X, to_matrix_gate
import qulacs.converter
import re
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime
import subprocess


class Runner:
    """A class to run the Quantum Volume algorithm and measure its performance using Qulacs.

    Attributes:
        n (int): The number of qubits.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        state (QuantumState): The Qulacs quantum state.
        circuit (QuantumCircuit): The Qulacs circuit for the Quantum Volume algorithm.
        ram_csv_file (str): The name of the CSV file to save RAM usage to.
    """
    
    def __init__(self, n: int, cores: int, ram_monitor, cpu_monitor, console: Console, ram_csv_file: str):
        """Initializes the Runner.

        Args:
            n (int): The number of qubits.
            cores (int): The number of CPU cores to use.
            ram_monitor (RAMMonitor): The RAM monitor to use.
            cpu_monitor (CPUMonitor): The CPU monitor to use.
            console (Console): The rich console object to use for output.
            ram_csv_file (str): The name of the CSV file to save RAM usage to.
        """
        self.n = n
        self.cores = cores
        self.ram_monitor = ram_monitor
        self.cpu_monitor = cpu_monitor
        self.console = console
        self.state = QuantumState(n)
        self.circuit = None
        self.ram_csv_file = ram_csv_file
        
    def build_qiskit_QV(self):
        """Builds a Quantum Volume circuit using Qiskit and saves it to a QASM file."""
        qiskitEnv = "/home/jesus-cerrudo/anaconda3/envs/Qiskit3/bin/python3"
        result = subprocess.run([qiskitEnv, "qiskitCircuitGenerator.py", str(self.n)], capture_output=True, text=True)

    def _build_circuit(self) -> QuantumCircuit:
        """Builds the Qulacs circuit for the Quantum Volume algorithm from a QASM file.

        Returns:
            QuantumCircuit: The Qulacs circuit for the Quantum Volume algorithm.
        """
        self.build_qiskit_QV()
        
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            try:
                with open("qv_circuit.qasm", "r") as f:
                    lines_check = [line.rstrip('\n') for line in f]
                if not lines_check:
                    self.build_qiskit_QV()
                    attempts += 1
                    continue
                match = re.search(r'qreg\s+q\[(\d+)\];', lines_check[2])
                if match and int(match.group(1)) == self.n:
                    break
                else:
                    self.build_qiskit_QV()
                    attempts += 1
            except Exception:
                self.build_qiskit_QV()
                attempts += 1
        else:
            print(f"Se ha superado el número máximo de intentos ({max_attempts}) para generar el circuito QASM correctamente.")
            exit(1)
        
        with open("qv_circuit.qasm", "r") as file:
            lines = [line.rstrip('\n') for line in file]

        for i, line in enumerate(lines):
            if line.strip().startswith('u'):
                line = re.sub(r'-1\*pi/3', str(-math.pi / 3), line)
                line = re.sub(r'1\*pi/3', str(math.pi / 3), line)
                line = re.sub(r'pi/3', str(math.pi / 3), line)
                line = re.sub(r'-1\*pi/2', str(-math.pi / 2), line)
                line = re.sub(r'1\*pi/2', str(math.pi / 2), line)
                line = re.sub(r'-1\*pi', str(-math.pi), line)
                line = re.sub(r'1\*pi', str(math.pi), line)
                line = re.sub(r'pi/2', str(math.pi / 2), line)
                line = re.sub(r'pi', str(math.pi), line)
                line = re.sub(r'\)\s+q', ')q', line)
                lines[i] = line
        
        qc = qulacs.converter.convert_QASM_to_qulacs_circuit(lines)
        
        return qc

    def _run_simulation(self, num_iterations: int) -> list[float]:
        """Runs the simulation a given number of times and returns the execution times.

        Args:
            num_iterations (int): The number of times to run the simulation.

        Returns:
            list[float]: A list of execution times in nanoseconds.
        """
        
        times = []
        for _ in range(num_iterations):
            self.circuit = self._build_circuit()
            self.state.set_zero_state()
            t1 = time.perf_counter_ns()
            self.circuit.update_quantum_state(self.state)
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
