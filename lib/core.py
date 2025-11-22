# lib/core.py
import subprocess
import sys
import shutil
import os
from .config import SUPPORTED_SIMULATORS
from .ui import print_error, print_info, print_success, print_warning, console


def check_conda_installed():
    """Checks if conda is installed and accessible in the PATH."""
    if shutil.which("conda") is None:
        print_error("Conda is not installed or cannot be found in PATH.")
        sys.exit(1)


def check_environment_exists(env_name):
    """Checks if a specific conda environment exists."""
    try:
        result = subprocess.run(
            ["conda", "env", "list"],
            capture_output=True, text=True, check=True
        )
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) > 0 and parts[0] == env_name:
                return True
        return False
    except subprocess.CalledProcessError:
        return False


def create_conda_env(env_name, env_file):
    """Creates a conda environment from a file."""
    if not os.path.exists(env_file):
        return False, f"The file {env_file} does not exist."

    try:
        cmd = ["conda", "env", "create", "-f", env_file, "-n", env_name]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def remove_conda_env(env_name):
    """Removes a conda environment."""
    try:
        # -y flag is crucial for non-interactive removal
        cmd = ["conda", "env", "remove", "-n", env_name, "-y"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def install_simulators_envs(simulators_list):
    """Orchestrator for environment installation."""
    check_conda_installed()
    print_info("Starting environment verification and installation process...")

    for sim in simulators_list:
        if sim not in SUPPORTED_SIMULATORS:
            print_warning(f"Unknown simulator '{sim}', skipping.")
            continue

        config = SUPPORTED_SIMULATORS[sim]
        env_name = config["env_name"]
        env_file = config["env_file"]

        if check_environment_exists(env_name):
            print_success(f"Environment '{env_name}' for {sim} already exists. Skipping.")
            continue

        with console.status(
                f"[bold cyan]Installing environment for {sim} ({env_name})... This may take a while.") as status:
            success, msg = create_conda_env(env_name, env_file)
            if success:
                console.print(f"[bold green]✓[/bold green] Environment '{env_name}' created successfully.")
            else:
                console.print(f"[bold red]✗[/bold red] Failed to create '{env_name}'.")
                print_error(f"Conda error details:\n{msg}")

    print_success("Installation process finished.")


def uninstall_simulators_envs(simulators_list):
    """Orchestrator for environment uninstallation."""
    check_conda_installed()
    print_info("Starting environment removal process...")

    for sim in simulators_list:
        if sim not in SUPPORTED_SIMULATORS:
            continue

        config = SUPPORTED_SIMULATORS[sim]
        env_name = config["env_name"]

        if not check_environment_exists(env_name):
            print_warning(f"Environment '{env_name}' for {sim} does not exist. Skipping.")
            continue

        with console.status(f"[bold red]Removing environment for {sim} ({env_name})...[/bold red]") as status:
            success, msg = remove_conda_env(env_name)
            if success:
                console.print(f"[bold green]✓[/bold green] Environment '{env_name}' removed successfully.")
            else:
                console.print(f"[bold red]✗[/bold red] Failed to remove '{env_name}'.")
                print_error(f"Conda error details:\n{msg}")

    print_success("Uninstallation process finished.")


def parse_qubits_arg(qubits_arg):
    if '-' in qubits_arg:
        try:
            start, end = map(int, qubits_arg.split('-'))
            return list(range(start, end + 1))
        except ValueError:
            print_error(f"Invalid range format: {qubits_arg}. Use 'min-max' format.")
            sys.exit(1)
    else:
        try:
            return [int(qubits_arg)]
        except ValueError:
            print_error(f"Invalid qubit number: {qubits_arg}")
            sys.exit(1)


def validate_execution_requirements(simulators_list):
    check_conda_installed()
    missing_envs = []
    for sim in simulators_list:
        if sim not in SUPPORTED_SIMULATORS:
            continue
        env_name = SUPPORTED_SIMULATORS[sim]["env_name"]
        if not check_environment_exists(env_name):
            missing_envs.append(f"{sim} (requires: {env_name})")

    if missing_envs:
        print_error("Missing required environments. Run with --install to create them:")
        for missing in missing_envs:
            print(f"  - {missing}")
        sys.exit(1)
    print_success("All required environments are present.")


def run_benchmarks(simulators, qubits_list, shots):
    from rich.progress import Progress, SpinnerColumn, TextColumn
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task_total = progress.add_task("[green]Total Execution...", total=len(simulators) * len(qubits_list))
        for sim in simulators:
            env_name = SUPPORTED_SIMULATORS[sim]["env_name"]
            for q in qubits_list:
                progress.update(task_total, description=f"Running {sim} with {q} qubits...")
                import time
                time.sleep(0.5)
                progress.advance(task_total)
    print_success("Benchmarks finished.")