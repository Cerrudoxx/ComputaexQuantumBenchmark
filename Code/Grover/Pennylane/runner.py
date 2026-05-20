import psutil
import pennylane as qml
import numpy as np
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime
from collections import Counter

class Runner:
    """A class to run Grover's algorithm and measure its performance using Pennylane.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        device (Device): The Pennylane device to run the circuit on.
        circuit (QNode): The Pennylane QNode representing the circuit.
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
        self.device = qml.device("default.qubit", wires=n, shots=num_iterations)
        self.circuit = self._build_circuit()
        self.ram_csv_file = ram_csv_file

    def _build_circuit(self):
        """Builds the Pennylane circuit for Grover's algorithm.

        Returns:
            QNode: The Pennylane QNode representing the circuit.
        """
        optimal_num_iterations = math.floor(math.pi / (4 * math.asin(math.sqrt(1 / 2**self.n))))
         
        @qml.qnode(self.device)
        def circuit():
            for qubit in range(self.n):
                qml.Hadamard(wires=qubit)
                
            for _ in range(optimal_num_iterations):
                qml.Hadamard(wires=self.n - 1)
                qml.MultiControlledX(wires=range(self.n), control_values=[1]*(self.n-1))
                qml.Hadamard(wires=self.n - 1)
                
                for qubit in range(self.n):
                    qml.Hadamard(wires=qubit)
                    qml.X(wires=qubit)
                qml.Hadamard(wires=self.n - 1)
                qml.MultiControlledX(wires=range(self.n), control_values=[1]*(self.n-1))
                qml.Hadamard(wires=self.n - 1)
                for qubit in range(self.n):
                    qml.X(wires=qubit)
                    qml.Hadamard(wires=qubit)
            return qml.sample()
        
        return circuit

    def _run_simulation(self, num_executions: int) -> list[float]:
        """Runs the simulation a given number of times and returns the execution times.

        Args:
            num_executions (int): The number of times to run the simulation.

        Returns:
            list[float]: A list of execution times in nanoseconds.
        """
        times = []
        for _ in range(num_executions):
            t1 = time.perf_counter_ns()
            results=self.circuit()
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
