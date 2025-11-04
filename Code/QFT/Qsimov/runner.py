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
        """Runs the QFT algorithm and returns the results.

        Returns:
            dict: A dictionary containing the results of the execution.
        """
        self.console.print(f"Comienza la ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="green")

        
        if self.cpu_monitor:
            self.cpu_monitor.start()
        
        if self.ram_monitor:
            self.ram_monitor.start()
        n_iterations_in = 10
        t_for_loop = self._run_simulation(n_iterations_in)
        t_grover = statistics.mean(t_for_loop) / 1e9 if t_for_loop else 0
        std_grover = statistics.stdev(t_for_loop) / 1e9 if len(t_for_loop) > 1 else 0
        
        if t_grover > 8640:
            self.console.print(f"El algoritmo tarda más de un día en ejecutarse. Deteniendo la ejecución a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="red")
            exit(0)

        iterations_number = (math.ceil((2 * 1.96 * std_grover) / (0.05 * t_grover)) ** 2 
                             if t_grover > 0 else n_iterations_in)
        self.console.print(f"Optimal number of iterations: {iterations_number}", style="blue")

        if iterations_number > n_iterations_in:
            t_for_loop = (self._run_simulation(iterations_number - n_iterations_in) + 
                          self._run_simulation(n_iterations_in))
        else:
            iterations_number = n_iterations_in

        t_grover_final = statistics.mean(t_for_loop) / 1e9 if t_for_loop else 0
        std_grover_final = statistics.stdev(t_for_loop) / 1e9 if len(t_for_loop) > 1 else 0

        cpu_avg = self.cpu_monitor.average() if self.cpu_monitor else 0
        ram_avg = self.ram_monitor.average() if self.ram_monitor else 0
        ram_mb = self.ram_monitor.max_memory_usage_in_mb() if self.ram_monitor else 0
        max_ram_peak = self.ram_monitor.max_memory_usage() if self.ram_monitor else 0

        if self.cpu_monitor:
            self.cpu_monitor.stop()
        if self.ram_monitor:
            self.ram_monitor.stop()
            
        self.console.print(f"Termina la ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="green")

        return {
            'n': self.n,
            'iterations_number': iterations_number,  
            't_grover': t_grover_final,
            'std_grover': std_grover_final,
            'cpu_avg': cpu_avg,
            'ram_avg': ram_avg,
            'ram_mb': ram_mb,
            'max_ram_peak': max_ram_peak,
            'cores': self.cores
        }