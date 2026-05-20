import argparse
import os
import sys
import threading
from rich.console import Console
from Code.utils import ResourceMonitor
from .runner import Runner
from Code.utils.results_handler import ResultsHandler
import psutil

def set_active_cores(cores: int) -> int:
    """Sets the number of active CPU cores for the current process.

    Args:
        cores (int): The number of CPU cores to use.

    Returns:
        int: The number of active CPU cores.
    """
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
    """The main function for running the QFT algorithm with Qulacs."""
    parser = argparse.ArgumentParser(description="Run the Quantum Fourier Transform (QFT) with a specified number of qubits")
    parser.add_argument("n", type=str, help="Number of qubits or range (e.g., '4' or '4-7')")
    parser.add_argument("--cores", type=int, default=os.cpu_count(), help="Number of CPU cores to use")
    parser.add_argument("--no-ram", action='store_false', dest='ram', default=True, help="Do not monitor RAM")
    parser.add_argument("--no-cpu", action='store_false', dest='cpu', default=True, help="Do not monitor CPU")
    args = parser.parse_args()

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

    results_dir = f"results_{args.n}_qubits_{args.cores}_cores"
    index = 0
    base_dir = results_dir
    while os.path.exists(results_dir):
        index += 1
        results_dir = f"{base_dir}({index})"
    os.makedirs(results_dir)

    actual_cores = os.cpu_count()
    args.cores = min(args.cores, actual_cores)
    console = Console(record=True)
    console.print(f"Using {args.cores} cores", style="bold green")
    set_active_cores(args.cores)

    times_file_name = f'QFT_data_qulacs_{args.n}'
    results_handler = ResultsHandler(times_file_name, results_dir, console)

    for n in qubits_list:
        console.print(f"Running QFT with {n} qubits and {args.cores} cores...", style="bright_magenta")
        cpu_monitor = ResourceMonitor.CPUMonitor(interval=0.1) if args.cpu else None
        ram_monitor = ResourceMonitor.RAMMonitor(interval=0.1) if args.ram else None
        
        ram_csv_file = os.path.join(results_dir, f"ram_usage_n{n}.csv")
        grover_runner = Runner(n, args.cores, ram_monitor, cpu_monitor, console, ram_csv_file)
        results = grover_runner.run()
        
        results_handler.display_timing_table(results)
        results_handler.display_usage_table(results)
        results_handler.save_to_csv(results)

    if args.ram:
        ResourceMonitor.plot_ram_avg_from_results(os.path.join(results_dir, f"{times_file_name}.csv"))
        ResourceMonitor.plot_cpu_avg_from_results(os.path.join(results_dir, f"{times_file_name}.csv"))

    ResourceMonitor.plot_t_grover_from_csv(os.path.join(results_dir, f"{times_file_name}.csv"))

    results_handler.save_console_output()

if __name__ == "__main__":
    console = Console(record=True)
    main()