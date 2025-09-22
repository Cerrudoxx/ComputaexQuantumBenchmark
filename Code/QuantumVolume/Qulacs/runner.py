from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import Z, H, X, to_matrix_gate
import qulacs.converter
import re
import math
import statistics
import time
from rich.console import Console
import threading
from datetime import datetime
import subprocess


class Runner:
    """Clase para ejecutar el algoritmo de Grover y medir su rendimiento."""
    
    """Clase para ejecutar el algoritmo de Grover y medir su rendimiento."""
    
    def __init__(self, n: int, cores: int, ram_monitor, cpu_monitor, console: Console, ram_csv_file: str):
        self.n = n
        self.cores = cores
        self.ram_monitor = ram_monitor
        self.cpu_monitor = cpu_monitor
        self.console = console
        self.state = QuantumState(n)
        self.circuit = None
        self.ram_csv_file = ram_csv_file
        
    def build_qiskit_QV(self):
        qiskitEnv = "/home/jesus-cerrudo/anaconda3/envs/Qiskit3/bin/python3"
        #qiskitEnv = "/lusitania_homes/CenitS/jesus.cerrudo/.conda/envs/Qiskit3/bin/python"
        # Run the Qiskit example script
        result = subprocess.run([qiskitEnv, "qiskitCircuitGenerator.py", str(self.n)], capture_output=True, text=True)
        # subprocess.run() ya espera a que el subproceso termine antes de continuar.
        # No necesitas hacer nada más: el código siguiente se ejecutará solo cuando el subproceso haya finalizado.
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        print(result.returncode)

    def _build_circuit(self) -> QuantumCircuit:
        self.build_qiskit_QV()
        
        # Comprobar si el fichero no está vacío y si el número de qubits es correcto, con límite de intentos
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            try:
                with open("qv_circuit.qasm", "r") as f:
                    lines_check = [line.rstrip('\n') for line in f]
                if not lines_check:
                    # El fichero está vacío, regenerar el circuito
                    self.build_qiskit_QV()
                    attempts += 1
                    continue
                match = re.search(r'qreg\s+q\[(\d+)\];', lines_check[2])
                if match and int(match.group(1)) == self.n:
                    break
                else:
                    # El número de qubits no coincide, regenerar el circuito
                    self.build_qiskit_QV()
                    attempts += 1
            except Exception:
                # Si ocurre algún error, intentar regenerar el circuito
                self.build_qiskit_QV()
                attempts += 1
        else:
            print(f"Se ha superado el número máximo de intentos ({max_attempts}) para generar el circuito QASM correctamente.")
            exit(1)
        
        with open("qv_circuit.qasm", "r") as file:
            lines = [line.rstrip('\n') for line in file]

        # comprobar si la tercera linea contiene el numero correcto de qubits, sino, regenerar
    
        #Preprocesar las líneas
        for i, line in enumerate(lines):
            if line.strip().startswith('u'):
                line = re.sub(r'-1\*pi/3', str(-math.pi / 3), line)
                line = re.sub(r'1\*pi/3', str(math.pi / 3), line)
                line = re.sub(r'pi/3', str(math.pi / 3), line)
                line = re.sub(r'-1\*pi/2', str(-math.pi / 2), line)
                line = re.sub(r'1\*pi/2', str(math.pi / 2), line)
                line = re.sub(r'-1\*pi', str(-math.pi), line)
                line = re.sub(r'1\*pi', str(math.pi), line)
                line = re.sub(r'pi/2', str(math.pi / 2), line)
                line = re.sub(r'pi', str(math.pi), line)
                line = re.sub(r'\)\s+q', ')q', line)
                lines[i] = line
        # print("Líneas preprocesadas:", lines)
        
        # now = datetime.now()
        # print(f"Hora de preprocesado: {now.hour}:{now.minute}:{now.second}.{now.microsecond // 1000:03d}")
        
        qc = qulacs.converter.convert_QASM_to_qulacs_circuit(lines)
        
        return qc

    def _run_simulation(self, num_iterations: int) -> list[float]:
        """Ejecuta la simulación num_iterations veces y devuelve los tiempos."""
        
        times = []
        for _ in range(num_iterations):
            self.circuit = self._build_circuit()
            self.state.set_zero_state()  # Reiniciar el estado a |0>
            t1 = time.perf_counter_ns()
            self.circuit.update_quantum_state(self.state)
            t2 = time.perf_counter_ns()
            #print(self.state.get_vector())
            #t3 = time.perf_counter_ns()
            times.append(t2 - t1)
            #print(f"t2: {t3 - t2} ns")
        return times

    def run(self) -> dict:
        """Ejecuta el algoritmo de Grover y devuelve los resultados."""
        self.console.print(f"Comienza la ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="green")
        
        if self.cpu_monitor:
            self.cpu_monitor.start()
        
        # monitor_thread = None
        if self.ram_monitor:
            self.ram_monitor.start()
            # # Hilo para escribir en el archivo CSV (ajusta según tu implementación)
            # monitor_thread = threading.Thread(target=self.ram_monitor.real_time_memory_usage, 
            #                                 args=(self.ram_csv_file,))
            # monitor_thread.daemon = True
            # monitor_thread.start()
            
        # Iteraciones iniciales
        n_iterations_in = 10
        t_for_loop = self._run_simulation(n_iterations_in)
        t_grover = statistics.mean(t_for_loop) / 1e9 if t_for_loop else 0
        std_grover = statistics.stdev(t_for_loop) / 1e9 if len(t_for_loop) > 1 else 0
        
        #Si t_grover es mayor que 2,4 horas significa que el algoritmo tarda mas de un dia en ejecutar y se detiene de forma segura
        if t_grover > 8640:
            self.console.print(f"El algoritmo tarda más de un día en ejecutarse. Deteniendo la ejecución a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="red")
            exit(0)
            
        #Calcular iteraciones óptimas
        iterations_number = (math.ceil((2 * 1.96 * std_grover) / (0.05 * t_grover)) ** 2 
                            if t_grover > 0 else n_iterations_in)
        #iterations_number = 500
        self.console.print(f"Optimal number of iterations: {iterations_number}", style="blue")

        # Más iteraciones si es necesario
        if iterations_number > n_iterations_in:
            t_for_loop = (self._run_simulation(iterations_number - n_iterations_in) + 
                          self._run_simulation(n_iterations_in))
        else:
            iterations_number = n_iterations_in

        t_grover_final = statistics.mean(t_for_loop) / 1e9 if t_for_loop else 0
        std_grover_final = statistics.stdev(t_for_loop) / 1e9 if len(t_for_loop) > 1 else 0

        # Obtener métricas de recursos
        cpu_avg = self.cpu_monitor.average() if self.cpu_monitor else 0
        ram_avg = self.ram_monitor.average() if self.ram_monitor else 0
        ram_mb = self.ram_monitor.max_memory_usage_in_mb() if self.ram_monitor else 0
        max_ram_peak = self.ram_monitor.max_memory_usage() if self.ram_monitor else 0

        if self.cpu_monitor:
            self.cpu_monitor.stop()
        if self.ram_monitor:
            self.ram_monitor.stop()
            # if monitor_thread and monitor_thread.is_alive():
            #     monitor_thread.join()ç
            
        # Eliminar el contenido de qv_circuit.qasm
        with open("qv_circuit.qasm", "w") as f:
            f.truncate(0)
                
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
