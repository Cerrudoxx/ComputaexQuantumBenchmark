import psutil
import qibo
from qibo import Circuit, gates
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime
import subprocess

class Runner:
    """A class to run the Quantum Volume algorithm and measure its performance using Qibo.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of iterations to run the algorithm.
        cores (int): The number of CPU cores to use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        circuit (Circuit): The Qibo circuit for the Quantum Volume algorithm.
        ram_csv_file (str): The name of the CSV file to save RAM usage to.
    """
    qibo.set_backend("qibojit", platform="numba")
    qibo.set_device("/CPU:0")

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

    def build_qiskit_QV(self):
        """Builds a Quantum Volume circuit using Qiskit and saves it to a QASM file."""
        qiskitEnv = "/home/jesus-cerrudo/anaconda3/envs/Qiskit3/bin/python3"
        result = subprocess.run([qiskitEnv, "qiskitCircuitGenerator.py", str(self.n)], capture_output=True, text=True)

    def _build_circuit(self) -> Circuit:
        """Builds the Qibo circuit for the Quantum Volume algorithm from a QASM file.

        Returns:
            Circuit: The Qibo circuit for the Quantum Volume algorithm.
        """
        self.build_qiskit_QV()
        with open("qv_circuit.qasm", "r") as file:
            qasm_code = file.read()
        
        qc = Circuit.from_qasm(qasm_code)
        return qc

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
            self.circuit = self._build_circuit()
            t1 = time.perf_counter_ns()
            self.circuit()
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the Quantum Volume algorithm and returns the results.

        Returns:
            dict: A dictionary containing the results of the execution.
        """
        self.console.print(
            f"Comienza la ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"Número de qubits: {self.n} | Núcleos: {self.cores}",
            style="green"
        )

        process = psutil.Process()
        start_ctx = process.num_ctx_switches()
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
                          t_for_loop)
        else:
            iterations_number = n_iterations_in

        t_grover_final = statistics.mean(t_for_loop) / 1e9 if t_for_loop else 0
        std_grover_final = statistics.stdev(t_for_loop) / 1e9 if len(t_for_loop) > 1 else 0

        cpu_avg = self.cpu_monitor.average() if self.cpu_monitor else 0
        ram_avg = self.ram_monitor.average() if self.ram_monitor else 0
        ram_mb = self.ram_monitor.memory_usage_in_mb() if self.ram_monitor else 0
        max_ram_peak = self.ram_monitor.max_memory_usage() if self.ram_monitor else 0

        end_ctx = process.num_ctx_switches()
        ctx_switches_diff = (end_ctx.voluntary - start_ctx.voluntary) + (end_ctx.involuntary - start_ctx.involuntary)
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
            'cores': self.cores,
            'ctx_switches': ctx_switches_diff
        }