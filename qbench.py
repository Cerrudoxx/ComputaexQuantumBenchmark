import argparse
import subprocess
import sys
import os

def check_conda():
    """Check if conda is available."""
    try:
        subprocess.run(["conda", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: conda is not installed or not in PATH.")
        sys.exit(1)

def install_env(simulator):
    """Installs the conda environment for a specific simulator."""
    env_file = os.path.join("Envs", f"{simulator.lower()}_environment.yml")
    if not os.path.exists(env_file):
        print(f"Error: Environment file {env_file} not found.")
        sys.exit(1)
    
    print(f"Installing environment for {simulator} from {env_file}...")
    try:
        subprocess.run(["conda", "env", "create", "-f", env_file], check=True)
        print(f"Successfully installed environment for {simulator}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install environment: {e}")
        sys.exit(1)

def run_benchmark(algorithm, simulator, qubits, iterations, cores, no_ram, no_cpu):
    """Runs the benchmark in the specific conda environment."""
    # Map simulator to its environment name
    env_name = simulator.lower()
    if simulator.lower() == 'qiskit':
        env_name = 'qiskit'
    elif simulator.lower() == 'cirq':
        env_name = 'cirq'
    elif simulator.lower() == 'pennylane':
        env_name = 'pennylane'
    elif simulator.lower() == 'qibo':
        env_name = 'qibo'
    elif simulator.lower() == 'qsimov':
        env_name = 'qsimov'
    elif simulator.lower() == 'qulacs':
        env_name = 'qulacs'
    else:
        print(f"Warning: Unknown simulator '{simulator}'. Trying environment '{env_name}'.")

    # Map algorithm to directory
    algo_dir_map = {
        'grover': 'Grover',
        'qft': 'QFT',
        'quantumvolume': 'QuantumVolume'
    }
    
    algo_dir = algo_dir_map.get(algorithm.lower())
    if not algo_dir:
        print(f"Error: Unknown algorithm '{algorithm}'. Must be one of {list(algo_dir_map.keys())}")
        sys.exit(1)

    # Capitalize simulator for directory
    sim_dir = simulator.capitalize()
    
    if sim_dir == 'Iqs':
        sim_dir = 'IQS' # IQS is usually uppercase
        
    script_path = os.path.join("Code", algo_dir, sim_dir)
    if not os.path.exists(script_path):
        print(f"Error: Path {script_path} does not exist.")
        sys.exit(1)

    # Find the main file
    main_file = None
    for file in os.listdir(script_path):
        if file.endswith("_main.py") or file == f"{simulator.lower()}_main.py":
            main_file = os.path.join(script_path, file)
            break
            
    if not main_file:
        print(f"Error: Could not find a main script in {script_path}")
        sys.exit(1)

    print(f"Running {main_file} in environment {env_name}...")
    
    # Construct the python command
    cmd = [
        "conda", "run", "-n", env_name, "--no-capture-output", 
        "python", "-m", main_file.replace(os.path.sep, '.').replace('.py', ''),
        str(qubits), str(iterations)
    ]
    if cores:
        cmd.extend(["--cores", str(cores)])
    if no_ram:
        cmd.append("--no-ram")
    if no_cpu:
        cmd.append("--no-cpu")
        
    # We set PYTHONPATH to include the root directory so Code.utils works
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.path.dirname(__file__))

    try:
        subprocess.run(cmd, check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Benchmark execution failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="HPC-QuBench Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Env Install command
    parser_env = subparsers.add_parser("env", help="Environment management")
    env_subparsers = parser_env.add_subparsers(dest="env_command")
    
    parser_install = env_subparsers.add_parser("install", help="Install a conda environment")
    parser_install.add_argument("simulator", type=str, help="Name of the simulator (e.g., qiskit, cirq)")

    # Run command
    parser_run = subparsers.add_parser("run", help="Run a benchmark")
    parser_run.add_argument("algorithm", type=str, help="Algorithm to benchmark (grover, qft, quantumvolume)")
    parser_run.add_argument("simulator", type=str, help="Simulator to use (qiskit, cirq, pennylane, etc.)")
    parser_run.add_argument("--qubits", type=str, required=True, help="Number of qubits or range (e.g., '4' or '4-7')")
    parser_run.add_argument("--iterations", type=str, required=True, help="Number of iterations or range (e.g., '512' or '512-1024')")
    parser_run.add_argument("--cores", type=int, help="Number of CPU cores to use")
    parser_run.add_argument("--no-ram", action='store_true', help="Do not monitor RAM")
    parser_run.add_argument("--no-cpu", action='store_true', help="Do not monitor CPU")

    args = parser.parse_args()

    if args.command == "env" and args.env_command == "install":
        check_conda()
        install_env(args.simulator)
    elif args.command == "run":
        check_conda()
        run_benchmark(args.algorithm, args.simulator, args.qubits, args.iterations, args.cores, args.no_ram, args.no_cpu)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
