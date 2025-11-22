#!/usr/bin/env python3
import argparse
import sys
from lib.ui import show_header, show_menu, print_info, print_error, wait_for_user, print_success
from lib.config import SUPPORTED_SIMULATORS, get_available_simulators
from lib.core import (
    parse_qubits_arg,
    validate_execution_requirements,
    run_benchmarks,
    install_simulators_envs,
    uninstall_simulators_envs
)


def get_target_simulators(sims_arg):
    """Helper to resolve '*' or a list of simulators."""
    if not sims_arg or "*" in sims_arg:
        return get_available_simulators()

    normalized = [s.lower() for s in sims_arg]
    valid = []
    for s in normalized:
        if s in SUPPORTED_SIMULATORS:
            valid.append(s)
        else:
            print_error(f"Simulator '{s}' is invalid.")
    return valid


def main():
    parser = argparse.ArgumentParser(description="HPC-QuBench Centralized Runner")

    # Arguments
    parser.add_argument("simulators", nargs="*", help="List of simulators or '*' for all.")
    parser.add_argument("--install", action="store_true", help="Automatically install required Conda environments.")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall required Conda environments.")
    parser.add_argument("--qubits", help="Fixed number (e.g., 5) or range (e.g., 5-10).")
    parser.add_argument("--shots", type=int, default=1000, help="Number of shots for execution.")

    args = parser.parse_args()

    # --- INTERACTIVE MODE (Loop) ---
    if not args.simulators and not args.install and not args.uninstall:
        while True:
            choice = show_menu()

            if choice == "1":
                print_info("Assisted mode is under development.")
                print_info("Please use CLI mode for benchmark execution for now.")
                print_info("Example: python hpcqubench.py qiskit --qubits 10")
                wait_for_user()

            elif choice == "2":
                # Install all
                install_simulators_envs(get_available_simulators())
                wait_for_user()

            elif choice == "3":
                # Uninstall all
                uninstall_simulators_envs(get_available_simulators())
                wait_for_user()

            elif choice == "4":
                print_info(f"Available Simulators: {', '.join(get_available_simulators())}")
                wait_for_user()

            elif choice == "5":
                print_success("Exiting HPC-QuBench. Goodbye!")
                sys.exit(0)

    # --- CLI MODE (One-off execution) ---

    # Determine target simulators
    target_sims = []
    # If no simulators listed but install/uninstall is used, assume all (*).
    if not args.simulators and (args.install or args.uninstall):
        target_sims = get_available_simulators()
    else:
        target_sims = get_target_simulators(args.simulators)

    if not target_sims:
        print_error("No valid simulators selected.")
        sys.exit(1)

    # 1. Uninstall Mode
    if args.uninstall:
        show_header()
        print_info(f"Uninstalling environments for: {', '.join(target_sims)}")
        uninstall_simulators_envs(target_sims)
        sys.exit(0)

    # 2. Install Mode
    if args.install:
        show_header()
        print_info(f"Installing environments for: {', '.join(target_sims)}")
        install_simulators_envs(target_sims)
        if not args.qubits:
            sys.exit(0)

    # 3. Benchmark Execution
    if not args.qubits:
        print_error("You must specify --qubits to run benchmarks.")
        sys.exit(1)

    qubits_list = parse_qubits_arg(args.qubits)

    show_header()
    print_info(f"Simulators to run: {', '.join(target_sims)}")

    validate_execution_requirements(target_sims)
    run_benchmarks(target_sims, qubits_list, args.shots)


if __name__ == "__main__":
    main()