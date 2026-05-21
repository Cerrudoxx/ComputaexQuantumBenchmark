# Grover's Algorithm Simulation with Qsimov

This application implements Grover's algorithm using the **Qsimov** library for quantum simulation. It measures execution time and standard deviation across multiple runs, monitors CPU and RAM usage, context switches, saves results to CSV files, and generates a combined dashboard plot. The console output is enhanced using the **Rich** library for improved visualization and progress tracking.

## Usage

The application is executed from the command line using the unified `qbench.py` CLI script from the root directory:

```bash
python3 qbench.py run grover qsimov [OPTIONS]
```

### Options

- `--qubits`: Number of qubits or range of qubits (e.g., '4' or '4-7'). Must be greater than 2. Default: 4.
- `--iterations`: Number of iterations or range of iterations (e.g., '512' or '512-1024').
- `--cores`: Number of CPU cores to use (defaults to all available cores).

### Execution Examples

Run with 4 qubits, 512 iterations, and all available cores:
```bash
python3 qbench.py run grover qsimov --qubits 4 --iterations 512
```

Run with a qubit range from 4 to 7, iterations from 512 to 1024, and 2 cores:
```bash
python3 qbench.py run grover qsimov --qubits 4-7 --iterations 512-1024 --cores 2
```

## Description of Main Classes and Modules

### `benchmark_base.py`
- **Purpose**: Encapsulates the execution orchestration.
- **Key Methods**: Uses `rich.progress` to display animated Spinners and Progress Bars. It invokes the underlying framework's runner and coordinates metrics collection.

### GroverRunner (`grover_runner.py`)
- **Purpose**: Constructs and executes the quantum circuit for Grover's algorithm in Qsimov.
- **Key Methods**: 
  - `run()`: Executes the algorithm using the unified `Qsimov` backend. Stops execution if the estimated time exceeds one day.

### ResultsHandler (`results_handler.py`)
- **Purpose**: Manages the visualization of results in tables and saves them to CSV files using Rich Layouts.
- **Features**: Displays beautiful summaries of hardware, timing, CPU, RAM, and OS context switches. Saves the console output to an `out.txt` file.

### ResourceMonitor (`ResourceMonitor.py`)
- **Purpose**: Monitor CPU, RAM usage, and OS metrics (context switches) during execution using daemon threads.
- **Features**: Calculates P95, Median, Min, Max, and Standard Deviation.
- **Plotting**: Generates individual plots and a **2x2 Combined Dashboard** plot showing Time vs Qubits, Peak RAM, CPU Average, and OS Context switches.

## Output Files

Inside the automatically generated unique results directory (e.g. `results_4_qubits_512_iterations_16_cores/`):
- **Results CSV** (`Grover_data_qsimov_<n>.csv`): Contains comprehensive execution data.
- **Plots**:
  - `*_cpu_avg_qubits.png`: Plot of average CPU usage.
  - `*_ram_avg_qubits.png`: Plot of peak RAM usage.
  - `*_time_qubits.png`: Plot of execution time with standard deviation error bars.
  - `*_dashboard.png`: Unified 2x2 dashboard plot.
- **Console Output** (`out.txt`): Log of all console output including rich formatting.
