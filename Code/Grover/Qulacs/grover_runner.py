import psutil
from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import Z, H, X, to_matrix_gate
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime

class GroverRunner:
    """A class to run Grover's algorithm and measure its performance using Qulacs.

    Attributes:
        n (int): The number of qubits.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        state (QuantumState): The Qulacs quantum state.
        circuit (QuantumCircuit): The Qulacs circuit for Grover's algorithm.
        ram_csv_file (str): The name of the CSV file to save RAM usage to.
    """
    
    def __init__(self, n: int, cores: int, ram_monitor, cpu_monitor, console: Console, ram_csv_file: str):
        """Initializes the GroverRunner.

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
        self.circuit = self._build_circuit()
        self.ram_csv_file = ram_csv_file

    def _build_circuit(self) -> QuantumCircuit:
        """Builds the Qulacs circuit for Grover's algorithm.

        Returns:
            QuantumCircuit: The Qulacs circuit for Grover's algorithm.
        """
        qc = QuantumCircuit(self.n)
        optimal_num_iterations = math.floor(math.pi / (4 * math.asin(math.sqrt(1 / 2**self.n))))
        print(optimal_num_iterations)
        for i in range(self.n):
            qc.add_gate(H(i))
        
        for _ in range(optimal_num_iterations):
            cnz = to_matrix_gate(Z(self.n - 1))
            for i in range(self.n - 1):
                cnz.add_control_qubit(i, 1)
            qc.add_gate(cnz)
            
            for i in range(self.n):
                qc.add_gate(H(i))
                qc.add_gate(X(i))
            cnz = to_matrix_gate(Z(self.n - 1))
            for i in range(self.n - 1):
                cnz.add_control_qubit(i, 1)
            qc.add_gate(cnz)
            for i in range(self.n):
                qc.add_gate(X(i))
                qc.add_gate(H(i))
        
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
