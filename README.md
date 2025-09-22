# Computaex Quantum Benchmark Simulator

This repository contains Python and C++ implementations of quantum algorithms for benchmarking quantum simulators on the Lusitania supercomputer. It evaluates performance metrics (execution time, CPU, and RAM usage) for Grover's Algorithm, Quantum Fourier Transform (QFT), and Quantum Volume (QV) across 3 to 30 qubits, with limits of 2.4 hours per iteration and 32 GB memory to ensure fair resource usage.

The code uses a common interface (`_build_circuit` and `_run_simulation`) for consistent comparison across simulators: Qiskit, Qulacs, Qibo, Qsimov, Cirq, PennyLane, and Intel Quantum Simulator (IQS). Python-based simulators run in Conda environments; IQS uses C++.

## Features
- **Benchmark Algorithms**:
  - **Grover's Algorithm**: Searches an unordered database using oracle and diffuser operations, targeting the last state (e.g., |111⟩ for 3 qubits) with ≈ ⌊π/4 * √(2^n)⌋ iterations. Selected for its high complexity and entanglement, challenging beyond 4-5 qubits on real hardware.
  - **Quantum Fourier Transform (QFT)**: Quantum analog of the Discrete Fourier Transform, used in algorithms like Shor's. Low-depth, low-entanglement circuit. Uses built-in functions (Qiskit, Qibo, Cirq, PennyLane) or custom implementations (Qsimov, Qulacs).
  - **Quantum Volume (QV)**: Generates random square circuits (depth = qubits) to compare architectures. Circuits are created with Qiskit's generator, translated via QASM2, and dynamically generated per measurement.

- **Performance Measurement**: Uses Python's `time` for execution time and `psutil` for CPU/RAM usage. Tests increment qubits from 3 to 30, halting if time or memory limits are exceeded.

- **Simulators**:
  - **[Qiskit](https://qiskit.org/)**: IBM's open-source SDK for quantum programming and simulation, with qiskit-aer for high-performance.
  - **[Qulacs](https://qulacs.org/)**: C++/Python simulator optimized for large-scale circuits, with GPU support.
  - **[Qibo](https://qibo.science/)**: Full-stack framework with C++/CUDA backends for simulation and hardware control.
  - **[Qsimov](https://github.com/qsimov)**: Python/NumPy-based simulator from UCLM, focused on adaptability and parallelism.
  - **[Cirq](https://quantumai.google/cirq)**: Google's Python framework for NISQ circuits, supporting simulation and hardware.
  - **[PennyLane](https://pennylane.ai/)**: Xanadu's library for quantum ML/chemistry, integrating with simulators and hardware.
  - **[Intel Quantum Simulator (IQS)](https://github.com/intel/intel-qs)**: C++ simulator optimized for multi-core/multi-node architectures, using state-vector representation.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Cerrudox/ComputaexQuantumBenchmark.git
   cd ComputaexQuantumBenchmark
   ```

2. Set up Conda environment (for Python simulators):

   - The implementation of each simulator is located in `Code/<Algorithm>/<Simulator>/` (e.g., `Code/Grover/Qiskit/`, `Code/QFT/Qulacs/`).


## Usage
Run benchmarks via the main script in each simulator's folder (e.g., `grover_qiskit_main.py`, `qulacs_main.py`):

```bash
python Code/Grover/Qiskit/grover_qiskit_main.py 3-30 1024 
```

- Arguments: Specify qubits range (e.g., `3-30`) and other parameters as needed.
- Outputs: Performance data (execution time, CPU/RAM) saved to CSV in `Results/`, with plots generated via Matplotlib.

Example for Grover on Qiskit:
```python
from Code.Grover.Qiskit.grover_qiskit_main import run_benchmark
results = run_benchmark(max_qubits=10)
print(results)  # Execution time, CPU/RAM per qubit count
```

For QV, circuits are generated dynamically using Qiskit’s generator (`qiskitCircuitGenerator.py`) and translated for other simulators. All implementations ensure equivalent circuits.

## Structure
- `Code/`: Contains algorithm-specific directories:
  - `Grover/`: Grover's Algorithm implementations.
  - `QFT/`: Quantum Fourier Transform implementations.
  - `QuantumVolume/`: Quantum Volume random circuit implementations.
  - Each algorithm directory contains subdirectories for each simulator (e.g., `Qiskit/`, `Qulacs/`), with files:
    - `<simulator>_main.py`: Main script to run the benchmark.
    - `grover_runner.py`/`runner.py`: Executes the simulation logic.
    - `ResourceMonitor.py`: Tracks CPU, RAM, and execution time.
    - `results_handler.py`: Processes and saves results.
    - `qiskitCircuitGenerator.py` (for QV): Generates random circuits.
    - `intel-qs` (for IQS): C++ source code or build instructions.
- `Results/`: Stores output logs and plots.
- `README.markdown`: Project documentation.

## Contributing
TODO

## License
TODO (check individual simulator licenses for compatibility).

For issues, open a GitHub issue. Code is optimized for Lusitania HPC but extensible to other clusters.
