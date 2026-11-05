import math
import time

import prism_q
from prism_q import BackendKind, CircuitBuilder
from rich.console import Console


class Runner:
    """A class to run the Quantum Fourier Transform (QFT) and measure its performance using PRISM-Q.

    The statevector backend is pinned so that PRISM-Q is measured as a statevector
    simulator, like the other frameworks in this suite, rather than letting it pick
    a backend from the circuit structure.

    Attributes:
        n (int): The number of qubits.
        num_iterations (int): The number of shots sampled per execution.
        cores (int): The number of CPU threads PRISM-Q may use.
        ram_monitor (RAMMonitor): The RAM monitor to use.
        cpu_monitor (CPUMonitor): The CPU monitor to use.
        console (Console): The rich console object to use for output.
        circuit (prism_q.Circuit): The PRISM-Q circuit for the QFT.
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
        self.circuit = self._build_circuit()
        self.ram_csv_file = ram_csv_file

    def _build_circuit(self) -> prism_q.Circuit:
        """Builds the PRISM-Q circuit for the QFT.

        Same gate sequence as the Qulacs implementation: a Hadamard and controlled
        phases on each qubit from the highest index down, then swaps that reverse
        the qubit order.

        Returns:
            prism_q.Circuit: The PRISM-Q circuit for the QFT.
        """
        n = self.n
        qc = CircuitBuilder(n, n)

        for j in reversed(range(n)):
            qc.h(j)
            for k in range(j):
                qc.cphase(math.pi / 2 ** (j - k), k, j)

        for j in range(n // 2):
            qc.swap(j, n - j - 1)

        qc.measure_all()
        return qc.build()

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
            t1 = time.perf_counter_ns()
            self.pool.install(self._simulate)
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
