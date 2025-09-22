import argparse
import os
import sys
import threading
from rich.console import Console
import ResourceMonitor
from grover_runner import GroverRunner
from results_handler import ResultsHandler
import psutil

def set_active_cores(cores: int) -> int:
    """Configura el número de núcleos activos."""
    os.environ["OMP_NUM_THREADS"] = str(cores)
    os.environ["MKL_NUM_THREADS"] = str(cores)
    os.environ["NUMEXPR_NUM_THREADS"] = str(cores)
    os.environ["VECLIB_MAXIMUM_THREADS"] = str(cores)
    os.environ["OPENBLAS_NUM_THREADS"] = str(cores)
    
    actual_cores = os.cpu_count()
    if cores < actual_cores:

        p = psutil.Process()
        cores_to_use = list(range(cores))
        p.cpu_affinity(cores_to_use)
        console.print(f"Disabled {actual_cores - cores} cores, using cores: {cores_to_use}", style="bold blue")
        return cores
    return actual_cores

def main():
    parser = argparse.ArgumentParser(description="Run Grover's algorithm with a specified number of qubits")
    parser.add_argument("n", type=str, help="Number of qubits or range (e.g., '4' or '4-7')")
    parser.add_argument("--cores", type=int, default=os.cpu_count(), help="Number of CPU cores to use")
    parser.add_argument("--no-ram", action='store_false', dest='ram', default=True, help="Do not monitor RAM")
    parser.add_argument("--no-cpu", action='store_false', dest='cpu', default=True, help="Do not monitor CPU")
    args = parser.parse_args()

    # Parsear qubits
    if '-' in args.n:
        start, end = map(int, args.n.split('-'))
        if start >= end:
            print("Error: Invalid range of qubits.")
            sys.exit(1)
        qubits_list = range(start, end + 1)
    else:
        n = int(args.n)
        if n <= 2:
            print("Error: Number of qubits must be greater than 2.")
            sys.exit(1)
        qubits_list = [n]

    # Configurar directorio de resultados
    results_dir = f"results_{args.n}_qubits_{args.cores}_cores"
    index = 0
    base_dir = results_dir
    while os.path.exists(results_dir):
        index += 1
        results_dir = f"{base_dir}({index})"
    os.makedirs(results_dir)

    # Configurar núcleos
    actual_cores = os.cpu_count()
    args.cores = min(args.cores, actual_cores)
    console = Console(record=True)
    console.print(f"Using {args.cores} cores", style="bold green")
    set_active_cores(args.cores)

    # Inicializar manejador de resultados
    times_file_name = f'Grover_data_qulacs_{args.n}'
    results_handler = ResultsHandler(times_file_name, results_dir, console)

    # Monitoreo continuo de RAM
    # file_name = os.path.join(results_dir, f"grover_qulacs_{args.n}_qubits_{args.cores}_cores.csv")
    # if args.ram:
    #     ram_monitor_continuous = ResourceMonitor.RAMMonitor()
    #     monitor_thread = threading.Thread(target=ram_monitor_continuous.real_time_memory_usage, args=(file_name,))
    #     monitor_thread.daemon = True
    #     monitor_thread.start()

    # Ejecutar para cada n
    for n in qubits_list:
        console.print(f"Running Grover's algorithm with {n} qubits and {args.cores} cores...", style="bright_magenta")
        cpu_monitor = ResourceMonitor.CPUMonitor(interval=0.1) if args.cpu else None
        ram_monitor = ResourceMonitor.RAMMonitor(interval=0.1) if args.ram else None
        
        ram_csv_file = os.path.join(results_dir, f"ram_usage_n{n}.csv")
        grover_runner = GroverRunner(n, args.cores, ram_monitor, cpu_monitor, console, ram_csv_file)
        results = grover_runner.run()
        
        results_handler.display_timing_table(results)
        results_handler.display_usage_table(results)
        results_handler.save_to_csv(results)

    # Finalizar
    if args.ram:
        #ResourceMonitor.plot_ram_usage_from_csv(ram_csv_file)
        ResourceMonitor.plot_ram_avg_from_results(os.path.join(results_dir, f"{times_file_name}.csv"))

    ResourceMonitor.plot_t_grover_from_csv(os.path.join(results_dir, f"{times_file_name}.csv"))

    results_handler.save_console_output()

if __name__ == "__main__":
    console = Console(record=True)
    main()