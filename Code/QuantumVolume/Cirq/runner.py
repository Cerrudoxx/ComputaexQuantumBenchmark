import psutil
import cirq
import cirq_google
import numpy as np
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime
from collections import Counter
from cirq.contrib.qasm_import import circuit_from_qasm
import subprocess

class Runner:
    """A class to run the Quantum Volume algorithm and measure its performance using Cirq.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        qubits (list): A list of Cirq qubits.
        circuit (Circuit): The Cirq circuit for the Quantum Volume algorithm.
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
        self.qubits = [cirq.LineQubit(i) for i in range(n)]
        self.circuit = self._build_circuit()
        self.ram_csv_file = ram_csv_file

    def build_qiskit_QV(self):
        """Builds a Quantum Volume circuit using Qiskit and saves it to a QASM file."""
        qiskitEnv = "/home/jesus-cerrudo/anaconda3/envs/Qiskit3/bin/python3"
        result = subprocess.run([qiskitEnv, "qiskitCircuitGenerator.py", str(self.n)], capture_output=True, text=True)

    def _build_circuit(self):
        """Builds the Cirq circuit for the Quantum Volume algorithm from a QASM file.

        Returns:
            Circuit: The Cirq circuit for the Quantum Volume algorithm.
        """
        self.build_qiskit_QV()

        with open("qv_circuit.qasm", "r") as f:
            qasm_content = f.read()
        qasm_content = qasm_content.replace("u(", "u3(")
        circuit = circuit_from_qasm(qasm_content)

        circuit.append(cirq.measure(*circuit.all_qubits(), key='result'))
        
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
            self.circuit = self._build_circuit()
            simulator = cirq.Simulator()
            t1 = time.perf_counter_ns()
            result = simulator.run(self.circuit, repetitions=self.num_iterations)
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
