import argparse
import os
import sys
import threading
from rich.console import Console
import ResourceMonitor
from runner import Runner
from results_handler import ResultsHandler

def main():
    
    
    parser = argparse.ArgumentParser(description="Run Grover's algorithm with a specified number of qubits and iterations")
    parser.add_argument("n", type=str, help="Number of qubits or range (e.g., '4' or '4-7')")
    parser.add_argument("num_iterations", type=str, help="Number of iterations or range (e.g., '512' or '512-1024')")
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

    # Parsear iteraciones
    if '-' in args.num_iterations:
        start, end = map(int, args.num_iterations.split('-'))
        if start >= end:
            print("Error: Invalid range of iterations.")
            sys.exit(1)
        iterations_list = [2**i for i in range(start.bit_length() - 1, end.bit_length()) if 2**i >= start and 2**i <= end]
    else:
        num_iterations = int(args.num_iterations)
        if num_iterations == 0:
            print("Error: Number of iterations must be non-zero.")
            sys.exit(1)
        iterations_list = [num_iterations]

    # Configurar directorio de resultados
    results_dir = f"results_{args.n}_qubits_{args.num_iterations}_iterations_{args.cores}_cores"
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

    # Inicializar manejador de resultados
    times_file_name = f'Grover_data_qiskit_{args.n}'
    results_handler = ResultsHandler(times_file_name, results_dir, console)

    # Monitoreo continuo de RAM
    # file_name = os.path.join(results_dir, f"grover_qulacs_{args.n}_qubits_{args.cores}_cores.csv")
    # if args.ram:
    #     ram_monitor_continuous = ResourceMonitor.RAMMonitor()
    #     monitor_thread = threading.Thread(target=ram_monitor_continuous.real_time_memory_usage, args=(file_name,))
    #     monitor_thread.daemon = True
    #     monitor_thread.start()
        
    # Ejecutar para cada n y num_iterations
    for n in qubits_list:
        for num_iterations in iterations_list:
            console.print(f"Running Grover's algorithm with {n} qubits, {num_iterations} iterations, and {args.cores} cores...", style="bright_magenta")
            cpu_monitor = ResourceMonitor.CPUMonitor(interval=0.1) if args.cpu else None
            ram_monitor = ResourceMonitor.RAMMonitor(interval=0.1) if args.ram else None 
            
            ram_csv_file = os.path.join(results_dir, f"ram_usage_n{n}.csv")
            grover_runner = Runner(n, num_iterations, args.cores, ram_monitor, cpu_monitor, console, ram_csv_file)
            results = grover_runner.run()
            
            results_handler.display_timing_table(results)
            results_handler.display_usage_table(results)
            results_handler.save_to_csv(results)
    if args.ram:
        #ResourceMonitor.plot_ram_usage_from_csv(ram_csv_file)
        ResourceMonitor.plot_ram_avg_from_results(os.path.join(results_dir, f"{times_file_name}.csv"))

    ResourceMonitor.plot_t_grover_from_csv(os.path.join(results_dir, f"{times_file_name}.csv"))
    
    #ResourceMonitor.plot_t_grover_from_csv(os.path.join(results_dir, f"{times_file_name}.csv"))
    # Finalizar
    results_handler.save_console_output()
if __name__ == "__main__":
    main()