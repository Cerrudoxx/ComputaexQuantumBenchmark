#!/usr/bin/env python3
"""Refactor all runner.py files: replace the entire run() method body
with a single delegation to benchmark_base.run_benchmark()."""

import os
import re

ROOT = '/home/jesus-cerrudo/Escritorio/Computaex/HPC-QuBench/ComputaexQuantumBenchmark'

runners = [
    'Code/Grover/Cirq/runner.py',
    'Code/Grover/Pennylane/runner.py',
    'Code/Grover/Qibo/grover_runner.py',
    'Code/Grover/Qiskit/grover_runner.py',
    'Code/Grover/Qsimov/grover_runner.py',
    'Code/Grover/Qulacs/grover_runner.py',
    'Code/QFT/Cirq/runner.py',
    'Code/QFT/Pennylane/runner.py',
    'Code/QFT/Qibo/runner.py',
    'Code/QFT/Qiskit/runner.py',
    'Code/QFT/Qsimov/runner.py',
    'Code/QFT/Qulacs/runner.py',
    'Code/QuantumVolume/Cirq/runner.py',
    'Code/QuantumVolume/Pennylane/runner.py',
    'Code/QuantumVolume/Qibo/runner.py',
    'Code/QuantumVolume/Qiskit/runner.py',
    'Code/QuantumVolume/Qsimov/runner.py',
    'Code/QuantumVolume/Qulacs/runner.py',
]

NEW_RUN = '''    def run(self) -> dict:
        """Runs the algorithm using the shared benchmark harness with Rich progress."""
        from Code.utils.benchmark_base import run_benchmark
        return run_benchmark(self, self.console)
'''

for rel in runners:
    fp = os.path.join(ROOT, rel)
    with open(fp, 'r') as f:
        content = f.read()

    if 'benchmark_base' in content:
        print(f"  SKIP (already done): {rel}")
        continue

    # Find the run() method and replace everything from its def to the end of class
    # Pattern: from `    def run(self)` to either the next `    def ` at same indent,
    # `class `, or end of file.
    pattern = re.compile(
        r'(    def run\(self\).*?\n)'   # the def line
        r'(.*?)(?=\n    def |\nclass |\Z)',  # body until next method/class/EOF
        re.DOTALL
    )

    match = pattern.search(content)
    if not match:
        print(f"  SKIP (no run()): {rel}")
        continue

    content = content[:match.start()] + NEW_RUN + content[match.end():]

    with open(fp, 'w') as f:
        f.write(content)
    print(f"  ✓ {rel}")

print("\nDone refactoring runners.")
