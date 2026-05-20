import psutil
import qibo
from qibo import Circuit, gates
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime

class GroverRunner:
    """A class to run Grover's algorithm and measure its performance using Qibo.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        circuit (Circuit): The Qibo circuit for Grover's algorithm.
        ram_csv_file (str): The name of the CSV file to save RAM usage to.
    """
    
    def __init__(self, n: int, num_iterations: int, cores: int, ram_monitor, cpu_monitor, console: Console, ram_csv_file: str):
        """Initializes the GroverRunner.

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

    def _build_circuit(self) -> Circuit:
        """Builds the Qibo circuit for Grover's algorithm.

        Returns:
            Circuit: The Qibo circuit for Grover's algorithm.
        """
        c = Circuit(self.n)
        optimal_num_iterations = math.floor(math.pi / (4 * math.asin(math.sqrt(1 / 2**self.n))))
        
        for qubit in range(self.n):
            c.add(gates.H(qubit))
        
        for _ in range(optimal_num_iterations):
            c.add(gates.Z(self.n - 1).controlled_by(*range(self.n - 1)))
            for qubit in range(self.n):
                c.add(gates.H(qubit))
            for qubit in range(self.n):
                c.add(gates.X(qubit))
            c.add(gates.Z(self.n - 1).controlled_by(*range(self.n - 1)))
            for qubit in range(self.n):
                c.add(gates.X(qubit))
            for qubit in range(self.n):
                c.add(gates.H(qubit))
        
        c.add(gates.M(*range(self.n)))
        return c

    def _run_simulation(self, num_executions: int) -> list[float]:
        """Runs the simulation a given number of times and returns the execution times.

        Args:
            num_executions (int): The number of times to run the simulation.

        Returns:
            list[float]: A list of execution times in nanoseconds.
        """
        qibo.set_threads(self.cores)
        times = []
        for _ in range(num_executions):
            t1 = time.perf_counter_ns()
            self.circuit()
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
