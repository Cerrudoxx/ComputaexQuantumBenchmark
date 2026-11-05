import time

import prism_q
from prism_q import BackendKind
from qiskit import qasm2
from qiskit.circuit.library import QuantumVolume as QV
from rich.console import Console


class Runner:
    """A class to run the Quantum Volume algorithm and measure its performance using PRISM-Q.

    Circuits come from Qiskit's QuantumVolume generator, exported to OpenQASM 2 and
    parsed by PRISM-Q, so every framework simulates the same random square circuit
    family. A fresh circuit is generated per execution, outside the timed region.

    The statevector backend is pinned so that PRISM-Q is measured as a statevector
    simulator, like the other frameworks in this suite.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of shots sampled per execution.
        cores (int): The number of CPU threads PRISM-Q may use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        circuit (prism_q.Circuit): The PRISM-Q circuit for the Quantum Volume algorithm.
        ram_csv_file (str): The name of the CSV file to save RAM usage to.
    """

    def __init__(self, n: int, num_iterations: int, cores: int, ram_monitor, cpu_monitor, console: Console, ram_csv_file: str):
        """Initializes the Runner.

        Args:
            n (int): The number of qubits.
            num_iterations (int): The number of shots sampled per execution.
            cores (int): The number of CPU threads PRISM-Q may use.
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
        self.pool = prism_q.ThreadPool(cores)
        self.circuit = None
        self.ram_csv_file = ram_csv_file

    def _build_circuit(self) -> prism_q.Circuit:
        """Builds a Quantum Volume circuit with Qiskit and converts it to PRISM-Q.

        Returns:
            prism_q.Circuit: The PRISM-Q circuit for the Quantum Volume algorithm.
        """
        qc = QV(num_qubits=self.n, depth=self.n).decompose(reps=5)
        qc.measure_all()
        return prism_q.parse_qasm(qasm2.dumps(qc))

    def _simulate(self):
        return (
            prism_q.simulate(self.circuit)
            .backend(BackendKind.statevector())
            .shots(self.num_iterations)
        )

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
            t1 = time.perf_counter_ns()
            self.pool.install(self._simulate)
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
