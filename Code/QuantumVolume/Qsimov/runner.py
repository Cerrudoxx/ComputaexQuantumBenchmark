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
import subprocess
import re

class Runner:    
    """A class to run the Quantum Volume algorithm and measure its performance using Qsimov.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        circuit (QCircuit): The Qsimov circuit for the Quantum Volume algorithm.
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
        
    
    def build_qiskit_QV(self):
        """Builds a Quantum Volume circuit using Qiskit and saves it to a QASM file."""
        qiskitEnv = "/home/jesus-cerrudo/anaconda3/envs/Qiskit3/bin/python3"
        result = subprocess.run([qiskitEnv, "qiskitCircuitGenerator.py", str(self.n)], capture_output=True, text=True)
        
    def translate_circuit(self, qc: qj.QCircuit) -> qj.QCircuit:
        """Translates a QASM circuit to a Qsimov circuit.

        Args:
            qc (qj.QCircuit): The Qsimov circuit to add the translated operations to.

        Returns:
            qj.QCircuit: The translated Qsimov circuit.
        """
        with open("qv_circuit.qasm", "r") as archivo:
         lineas = archivo.readlines()

        for linea in lineas[3:]:
            instruccion = linea.strip()

            if instruccion.startswith("u"):
                match = re.match(r'u\(([^,]+),([^,]+),([^)]+)\)\s+q\[(\d+)\];', instruccion)
                if match:
                    context = {"pi": math.pi}

                    theta = float(eval(match.group(1), {}, context))
                    phi = float(eval(match.group(2), {}, context))
                    lambd = float(eval(match.group(3), {}, context))
                    qubit = int(match.group(4))
                    
                    qc.add_operation('U('+str(theta)+','+str(phi)+','+str(lambd)+')',targets=qubit)
                else:
                    print(f"Instrucción U mal formada: {instruccion}")

            elif instruccion.startswith("cx"):
                match = re.match(r'cx\s+q\[(\d+)\],q\[(\d+)\];', instruccion)
                if match:
                    qubit1 = int(match.group(1))
                    qubit2 = int(match.group(2))
                    qc.add_operation('X',targets=qubit2,controls=qubit1)

                else:
                    print(f"Instrucción CX mal formada: {instruccion}")

            else:
                print(f"Instrucción no reconocida: {instruccion}")    
        return qc
        
    def _build_circuit(self) -> QCircuit:
        """Builds the Qsimov circuit for the Quantum Volume algorithm from a QASM file.

        Returns:
            QCircuit: The Qsimov circuit for the Quantum Volume algorithm.
        """
        self.build_qiskit_QV()
        qc= qj.QCircuit(self.n,self.n,'QV')
        qc = self.translate_circuit(qc)
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
            self.circuit = self._build_circuit()
            t1 = time.perf_counter_ns()
            result = self.executor.execute(self.circuit, iterations=self.num_iterations)
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
