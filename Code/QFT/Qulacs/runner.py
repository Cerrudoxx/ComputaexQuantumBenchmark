import psutil
from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import U1, Z, H, X, to_matrix_gate
import math
import statistics
import time
import numpy as np
from rich.console import Console
import threading
from datetime import datetime

class Runner:
    """A class to run the Quantum Fourier Transform (QFT) and measure its performance using Qulacs.

    Attributes:
        n (int): The number of qubits.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        state (QuantumState): The Qulacs quantum state.
        circuit (QuantumCircuit): The Qulacs circuit for the QFT.
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
        self.circuit = self._build_circuit()
        self.ram_csv_file = ram_csv_file

    def _build_circuit(self) -> QuantumCircuit:
        """Builds the Qulacs circuit for the QFT.

        Returns:
            QuantumCircuit: The Qulacs circuit for the QFT.
        """
        qc=QuantumCircuit(self.n)
        
        for j in reversed(range(self.n)):
            qc.add_H_gate(j)

            for k in range(j):
                gate=U1(j,np.pi/2**(j-k))
                gate = to_matrix_gate(gate)
                gate.add_control_qubit(k,1)
                qc.add_gate(gate=gate)
                
        for j in range(self.n//2):
            qc.add_SWAP_gate(j,self.n-j-1)
            
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
