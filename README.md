# Computaex Quantum Simulators Benchmark (HPC-QuBench)  ![alt text][logo]

## Project Overview
This repository provides a comprehensive framework for benchmarking quantum simulators using a suite of standard quantum algorithms. It is designed to evaluate and compare the performance of various quantum simulators on the Lusitania supercomputer, focusing on metrics such as execution time, CPU usage, and RAM consumption. The benchmarks are implemented for Grover's Algorithm, the Quantum Fourier Transform (QFT), and Quantum Volume (QV), covering a range of circuit complexities and entanglement patterns.

The framework supports multiple quantum simulators, including Qiskit, Qulacs, Qibo, Qsimov, Cirq, PennyLane, and the Intel Quantum Simulator (IQS). Each simulator is tested across a range of 3 to 30 qubits, with built-in constraints to ensure fair and efficient resource utilization on shared high-performance computing (HPC) systems.

## Features
- **Benchmark Algorithms**:
  - **Grover's Algorithm**: A quantum search algorithm that demonstrates a quadratic speedup over classical search. It is known for its high complexity and entanglement, making it a challenging benchmark for simulators, especially as the number of qubits increases.
  - **Quantum Fourier Transform (QFT)**: The quantum analogue of the Discrete Fourier Transform, a fundamental building block in many quantum algorithms, including Shor's algorithm for factoring. The QFT circuit has a relatively low depth and entanglement.
  - **Quantum Volume (QV)**: A metric that measures the largest square circuit a quantum computer can successfully implement. The benchmark generates random square circuits (where the depth equals the number of qubits) to provide a comprehensive test of a simulator's performance.

- **Performance Measurement**: The framework uses Python's `time` module for precise execution time measurements and `psutil` for monitoring CPU, RAM usage, and OS context switches. The benchmarks are designed to incrementally increase the number of qubits from 3 to 30, with automatic termination if predefined time or memory limits are exceeded. New plots for CPU and RAM average consumption vs Qubits are generated automatically.

- **Supported Simulators**:
  - **[Qiskit](https://qiskit.org/)**: An open-source SDK for quantum computing developed by IBM.
  - **[Qulacs](https://qulacs.org/)**: A fast quantum circuit simulator for large-scale quantum circuits, with GPU support.
  - **[Qibo](https://qibo.science/)**: A full-stack quantum simulation framework with support for multiple backends, including CPUs and GPUs.
  - **[Qsimov](https://github.com/Mowstyl/QSimov)**: A flexible and adaptable quantum circuit simulator developed at UCLM, with a focus on parallelism.
  - **[Cirq](https://quantumai.google/cirq)**: A Python framework for creating, editing, and invoking Noisy Intermediate Scale Quantum (NISQ) circuits.
  - **[PennyLane](https://pennylane.ai/)**: A cross-platform Python library for differentiable programming of quantum computers.
  - **[Intel Quantum Simulator (IQS)](https://github.com/intel/intel-qs)**: A high-performance C++ simulator optimized for multi-core and multi-node architectures.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Cerrudox/ComputaexQuantumBenchmark.git
   cd ComputaexQuantumBenchmark
   ```

2. Set up the Conda environments for the Python-based simulators using the new CLI tool `qbench.py`:
   ```bash
   python3 qbench.py env install qiskit
   python3 qbench.py env install cirq
   python3 qbench.py env install pennylane
   python3 qbench.py env install qibo
   python3 qbench.py env install qsimov
   python3 qbench.py env install qulacs
   ```

3. For the Intel Quantum Simulator (IQS), you will need to compile the C++ source code. The source code and build instructions are located in the `Code/<Algorithm>/IQS/intel-qs` directories.

## Usage
The repository now includes a unified Command Line Interface (`qbench.py`) that simplifies running the benchmarks and manages Conda environments automatically.

To run a benchmark, use the following syntax:

```bash
python3 qbench.py run <algorithm> <simulator> --qubits <q> --iterations <i>
```

For example, to run the Grover's algorithm benchmark with Qiskit for 3 to 10 qubits with 1024 iterations:

```bash
python3 qbench.py run grover qiskit --qubits 3-10 --iterations 1024
```

The CLI handles activating the corresponding Conda environment automatically. The script will output the performance data (Time, CPU Avg, RAM Avg, Peak RAM, and Context Switches) to a CSV file in the `Results/` directory and generate plots of the results using Matplotlib.

For the Quantum Volume benchmarks, the circuits are generated dynamically using a Qiskit-based script (`qiskitCircuitGenerator.py`) and then translated to the target simulator's format.

### Intel Quantum Simulator (IQS) Specifics
Unlike the Python-based simulators, IQS relies on a customized C++ compilation workflow for its benchmarks. The repository contains a complete clone of IQS inside the `Code/<Algorithm>/IQS/intel-qs/` folders.

The IQS execution process involves:
1. **Circuit Generation**: A Python script (e.g., `generadorCircuitoGrover.py`) uses Qiskit to create the desired circuit and exports it to QASM format.
2. **Translation**: A custom Python translator (`funciones_traductor.py`) parses the QASM file and generates equivalent C++ code for IQS (`circuito.cpp`).
3. **Compilation**: A bash script (`scriptcompilacion.sh`) executes `make` to compile the generated C++ code into an executable.
4. **Execution**: The compiled binary (`circuito.exe`) is then run to perform the simulation.

Currently, this C++ workflow is **not** integrated into the `qbench.py` Python CLI tool. To benchmark IQS, you must navigate to the respective `intel-qs/examples/` directory and execute the customized bash scripts (e.g., `ejecucionGrover.sh`) manually.
## Repository Structure
- `Code/`: Contains the source code for the benchmark implementations, organized by algorithm and then by simulator.
  - `Grover/`: Implementations of Grover's Algorithm.
  - `QFT/`: Implementations of the Quantum Fourier Transform.
  - `QuantumVolume/`: Implementations of the Quantum Volume benchmark.
- `Results/`: The default directory for storing output logs, CSV files, and plots.
- `README.md`: This file.
- `environment-*.yml`: Conda environment files for each of the Python-based simulators.

## 🖋️ Citation

If you use this benchmarking suite or the datasets provided in this repository for your research, please cite our published paper in **SIMULATION**:

```bibtex
@article{doi:10.1177/00375497261438515,
  author = {Jesús Cerrudo-Herrera and Daniel Talaván-Vega and Paloma Rodríguez-Oliver and Ahmed Ziabat-Ziabat and Juan Antonio Rico-Gallego},
  title ={Benchmarking quantum computing statevector simulators on high-performance computing},
  journal = {SIMULATION},
  volume = {0},
  number = {0},
  pages = {00375497261438515},
  year = {2026},
  doi = {10.1177/00375497261438515},
  URL = {[https://doi.org/10.1177/00375497261438515](https://doi.org/10.1177/00375497261438515)},
  eprint = {[https://doi.org/10.1177/00375497261438515](https://doi.org/10.1177/00375497261438515)}
}
```
## License

The benchmarking suite and utility scripts (custom Python, C++, and Bash code) are licensed under the [MIT License](LICENSE).

**Third-Party Code:** This repository includes the source code for the [Intel Quantum Simulator (IQS)](https://github.com/intel/intel-qs) for benchmarking purposes. IQS is licensed under the **Apache License 2.0**. Its respective license and copyright notices are preserved within the `intel-qs` subdirectories.

For issues, please open a GitHub issue. The code is optimized for the Lusitania HPC environment but is designed to be extensible to other systems.


[logo]: https://github.com/Cerrudoxx/ComputaexQuantumBenchmark/blob/main/HPC-QuBench-Logo.png "HPC-QuBench Logo"
