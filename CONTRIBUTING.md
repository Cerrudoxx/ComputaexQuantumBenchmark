# Contributing to Computaex Quantum Benchmark

First off, thank you for considering contributing to this repository! Our goal is to provide the most comprehensive performance landscape for quantum statevector simulators on HPC environments.

We welcome contributions from the quantum computing and HPC community, including:
- Adding support for **new quantum circuit simulators**.
- Adding **new quantum algorithms** to the benchmarking suite.
- Optimizing existing execution scripts for specific HPC schedulers (Slurm, PBS, etc.).
- Bug fixes and documentation improvements.

## How to Contribute

### 1. Reporting Bugs & Suggesting Features
If you find a bug or have a suggestion for a new feature (like a new simulator to benchmark), please open an issue in the GitHub issue tracker. Include as much detail as possible, such as OS, Python version, HPC environment, and logs.

### 2. Making a Pull Request (PR)
If you want to contribute code:
1. **Fork** the repository to your own GitHub account.
2. **Clone** your fork locally.
3. **Create a branch** for your feature or bug fix (`git checkout -b feature/new-simulator`).
4. **Commit** your changes with clear, descriptive commit messages.
5. **Push** the branch to your fork (`git push origin feature/new-simulator`).
6. **Open a Pull Request** against the `main` branch of the original repository.

### Adding a New Simulator
If you are adding a new simulator, please ensure your PR includes:
- A `runner.py` script equivalent to the existing ones.
- The execution main script (e.g., `newsim_main.py`).
- Integration into the `ResourceMonitor.py` standard to capture RAM and execution time consistently.
- A brief mention in the README on how to install the dependencies for this new simulator.

### Code Style
Please adhere to PEP 8 standards for Python code. Keep your code clean, well-commented, and easily adaptable to different HPC node configurations.
