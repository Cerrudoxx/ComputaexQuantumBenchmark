import psutil
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import MCXGate
from qiskit.circuit.library import QuantumVolume as QV
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime


class Runner:
    """A class to run the Quantum Volume algorithm and measure its performance using Qiskit.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        qc (QuantumCircuit): The Qiskit quantum circuit for the Quantum Volume algorithm.
        ram_csv_file (str): The name of the CSV file to save RAM usage to.
    """
    
    def __init__(self, n: int, num_iterations: int, cores: int, ram_monitor, cpu_monitor, console: Console, ram_csv_file: str):
        """Initializes the Runner.

        Args:
            n (int): The number of qubits.
            num_iterations (int): The number of iterations to run the algorithm.
            cores (int): The number of CPU cores to use.
            ram_monitor (RAMMonitor): The RAM monitor to use.
            cpu_monitor (CPUMonitor): The CPU monitor to use.
            console (Console): The rich console object to use for output.
            ram_csv_file (str): The name of the CSV file to save RAM usage to.
        """
        self.n = n
        self.num_iterations = num_iterations
        self.cores = cores
        self.ram_monitor = ram_monitor
        self.cpu_monitor = cpu_monitor
        self.console = console
        self.qc = None
        self.ram_csv_file = ram_csv_file
    
    def _build_circuit(self) -> QuantumCircuit:
        """Builds the Qiskit quantum circuit for the Quantum Volume algorithm.

        Returns:
            QuantumCircuit: The Qiskit quantum circuit for the Quantum Volume algorithm.
        """
        qc = QV(num_qubits=self.n, depth=self.n)
        qc.measure_all()
        return qc

    def _run_simulation(self, num_executions: int) -> list[float]:
        """Runs the simulation a given number of times and returns the execution times.

        Args:
            num_executions (int): The number of times to run the simulation.

        Returns:
            list[float]: A list of execution times in nanoseconds.
        """
        
        simulator = AerSimulator(method='statevector')
        simulator.set_options(max_parallel_threads=self.cores)
        times = []
        for _ in range(num_executions):
            self.qc = self._build_circuit()
            t1 = time.perf_counter_ns()
            transpiled_qc = transpile(self.qc, simulator)
            simulator.run([transpiled_qc], shots=self.num_iterations).result()
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
