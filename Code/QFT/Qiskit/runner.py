import psutil
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import MCXGate
from qiskit.circuit.library import QFT
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime


class Runner:
    """A class to run the Quantum Fourier Transform (QFT) and measure its performance using Qiskit.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        qc (QuantumCircuit): The Qiskit quantum circuit for the QFT.
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
        self.qc = self._build_circuit()
        self.ram_csv_file = ram_csv_file

    def _build_circuit(self) -> QuantumCircuit:
        """Builds the Qiskit quantum circuit for the QFT.

        Returns:
            QuantumCircuit: The Qiskit quantum circuit for the QFT.
        """
        qc=QFT(self.n, approximation_degree=0)
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
            t1 = time.perf_counter_ns()
            transpiled_qc = transpile(self.qc, simulator, optimization_level=3)
            result = simulator.run([transpiled_qc], shots=self.num_iterations).result()
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
