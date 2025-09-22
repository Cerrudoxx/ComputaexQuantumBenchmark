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
    """Clase para ejecutar el algoritmo de Grover y medir su rendimiento."""
    
    def __init__(self, n: int, num_iterations: int, cores: int, ram_monitor, cpu_monitor, console: Console, ram_csv_file: str):
        self.n = n
        self.num_iterations = num_iterations
        self.cores = cores
        self.ram_monitor = ram_monitor
        self.cpu_monitor = cpu_monitor
        self.console = console
        self.qc = self._build_circuit()
        self.ram_csv_file = ram_csv_file

    def _build_circuit(self) -> QuantumCircuit:
        qc=QFT(self.n, approximation_degree=0)
        qc.measure_all()
        return qc

    def _run_simulation(self, num_executions: int) -> list[float]:
        """Ejecuta la simulación num_executions veces y devuelve los tiempos."""
        simulator = AerSimulator(method='statevector')
        simulator.set_options(max_parallel_threads=self.cores)
        transpiled_qc = transpile(self.qc, simulator, optimization_level=3)
        #print(self.cores)
        #simulator.set_options(max_parallel_threads=self.cores)
        times = []
        for _ in range(num_executions):
            t1 = time.perf_counter_ns()
            result = simulator.run([transpiled_qc], shots=self.num_iterations).result()
            # print(result.get_counts())
            t2 = time.perf_counter_ns()
            times.append(t2 - t1)
        return times

    def run(self) -> dict:
        self.console.print(f"Comienza la ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="green")

        # Iniciar monitoreo de CPU
        if self.cpu_monitor:
            self.cpu_monitor.start()
        
        # Iniciar monitoreo de RAM si existe(se ha desactivado por defecto)
        # monitor_thread = None
        if self.ram_monitor:
            self.ram_monitor.start()
            # Hilo para escribir en el archivo CSV (ajusta según tu implementación)
            # monitor_thread = threading.Thread(target=self.ram_monitor.real_time_memory_usage, 
            #                                 args=(self.ram_csv_file,))
            # monitor_thread.daemon = True
            # monitor_thread.start()

        # Ejecutar la simulación
        n_iterations_in = 10
        t_for_loop = self._run_simulation(n_iterations_in)
        t_grover = statistics.mean(t_for_loop) / 1e9 if t_for_loop else 0
        std_grover = statistics.stdev(t_for_loop) / 1e9 if len(t_for_loop) > 1 else 0
        
        #Si t_grover es mayor que 2,4 horas significa que el algoritmo tarda mas de un dia en ejecutar y se detiene
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

        # Obtener métricas de recursos
        cpu_avg = self.cpu_monitor.average() if self.cpu_monitor else 0
        ram_avg = self.ram_monitor.average() if self.ram_monitor else 0
        ram_mb = self.ram_monitor.max_memory_usage_in_mb() if self.ram_monitor else 0
        max_ram_peak = self.ram_monitor.max_memory_usage() if self.ram_monitor else 0

        # Detener monitoreo
        if self.cpu_monitor:
            self.cpu_monitor.stop()
        if self.ram_monitor:
            self.ram_monitor.stop()
            # if monitor_thread and monitor_thread.is_alive():
            #     monitor_thread.join()
                
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
        
