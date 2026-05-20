import psutil
from qsimov import *
import qsimov as qj
import math
import statistics
import time
from rich.console import Console
import numpy as np
from typing import List
import threading
from datetime import datetime
from collections import Counter

class Runner:    
    """A class to run the Quantum Fourier Transform (QFT) and measure its performance using Qsimov.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        circuit (QCircuit): The Qsimov circuit for the QFT.
        executor (Drewom): The Qsimov executor to run the circuit.
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
        self.circuit = self._build_circuit()
        self.ram_csv_file = ram_csv_file

        # Create the quantum machine
        self.executor = qj.Drewom(qmachine="doki",
                            extra={"num_threads": self.cores,
                                    "random_generator": np.random.rand,
                                    "use_system": False,
                                    "return_struct": True})
        
    def _build_circuit(self) -> QCircuit:
        """Builds the Qsimov circuit for the QFT.

        Returns:
            QCircuit: The Qsimov circuit for the QFT.
        """
        qc= qj.QCircuit(self.n,self.n,'QFT')
        for j in reversed(range(self.n)):
            qc.add_operation('H',targets=j)
            for k in range(j):
                qc.add_operation('Rz('+str(np.pi/2**(j-k))+')',targets=k,controls=j)
        for j in range(self.n//2):
                qc.add_operation('Swap',targets=(j,self.n-j-1))
        targets = [i for i in range(self.n)]
        qc.add_operation("MEASURE", targets=targets, outputs=targets)
        return qc
    
    def _run_simulation(self, num_executions: int) -> List[float]:
        """Runs the simulation a given number of times and returns the execution times.

        Args:
            num_executions (int): The number of times to run the simulation.

        Returns:
            list[float]: A list of execution times in nanoseconds.
        """
        times = []
        for _ in range(num_executions):
            t1 = time.perf_counter_ns()
            result = self.executor.execute(self.circuit, iterations=self.num_iterations)
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
