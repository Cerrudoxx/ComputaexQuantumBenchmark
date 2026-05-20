#!/usr/bin/env python3
"""Refactor all *_main.py files to use the new Rich display methods."""

import os
import re

ROOT = '/home/jesus-cerrudo/Escritorio/Computaex/HPC-QuBench/ComputaexQuantumBenchmark'

mains = []
for root, _, files in os.walk(os.path.join(ROOT, 'Code')):
    if 'utils' in root or 'IQS' in root or '__pycache__' in root:
        continue
    for f in files:
        if f.endswith('_main.py'):
            mains.append(os.path.join(root, f))

mains.sort()

for fp in mains:
    with open(fp, 'r') as f:
        content = f.read()

    if 'display_header' in content:
        print(f"  SKIP (already done): {fp}")
        continue

    # Determine algorithm and simulator from path
    parts = fp.replace(ROOT + '/', '').split('/')
    algo = parts[1]  # Grover, QFT, QuantumVolume
    sim  = parts[2]  # Qiskit, Cirq, etc.

    # 1. Add Status import
    if 'from rich.status import Status' not in content:
        content = content.replace(
            'from rich.console import Console',
            'from rich.console import Console\nfrom rich.status import Status'
        )

    # 2. Replace "Using X cores" with nothing (display_header will show it)
    content = re.sub(
        r"    console\.print\(f\"Using \{args\.cores\} cores\".*?\n",
        "",
        content
    )

    # 3. Replace the inner loop print + runner creation + display calls
    # Pattern for the inner loop body
    old_inner = re.compile(
        r"(            )console\.print\(f\"Running .+?\n"
        r"\1cpu_monitor = .+?\n"
        r"\1ram_monitor = .+?\n"
        r"(?:\1\n)?"
        r"\1ram_csv_file = .+?\n"
        r"\1(\w+) = (\w+)\((.+?)\)\n"
        r"\1results = \2\.run\(\)\n"
        r"(?:\1\n)?"
        r"\1results_handler\.display_timing_table\(results\)\n"
        r"\1results_handler\.display_usage_table\(results\)\n"
        r"\1results_handler\.save_to_csv\(results\)",
        re.MULTILINE
    )

    match = old_inner.search(content)
    if match:
        indent = match.group(1)
        var_name = match.group(2)
        class_name = match.group(3)
        constructor_args = match.group(4)

        new_inner = f"""{indent}results_handler.display_header("{algo}", "{sim}", n, num_iterations, args.cores)
{indent}cpu_monitor = ResourceMonitor.CPUMonitor(interval=0.1) if args.cpu else None
{indent}ram_monitor = ResourceMonitor.RAMMonitor(interval=0.1) if args.ram else None
{indent}ram_csv_file = os.path.join(results_dir, f"ram_usage_n{{n}}.csv")
{indent}{var_name} = {class_name}({constructor_args})

{indent}with Status("[bold bright_cyan]⚛  Initializing quantum circuit...[/]", console=console, spinner="dots"):
{indent}    import time as _t; _t.sleep(0.5)

{indent}results = {var_name}.run()

{indent}results_handler.display_timing_table(results)
{indent}results_handler.display_usage_table(results)
{indent}results_handler.display_run_summary(results)
{indent}results_handler.save_to_csv(results)"""
        content = content[:match.start()] + new_inner + content[match.end():]
    else:
        print(f"  WARN (could not match inner loop): {fp}")

    # 4. Add dashboard plot call
    if 'plot_combined_dashboard' not in content:
        content = content.replace(
            '    ResourceMonitor.plot_t_grover_from_csv(',
            '    ResourceMonitor.plot_combined_dashboard(os.path.join(results_dir, f"{times_file_name}.csv"))\n    ResourceMonitor.plot_t_grover_from_csv('
        )
        # Also try the variant name used in Cirq files
        content = content.replace(
            '    ResourceMonitor.plot_t_from_csv(',
            '    ResourceMonitor.plot_combined_dashboard(os.path.join(results_dir, f"{times_file_name}.csv"))\n    ResourceMonitor.plot_t_from_csv('
        )

    with open(fp, 'w') as f:
        f.write(content)
    print(f"  ✓ {fp}")

print("\nDone refactoring mains.")
