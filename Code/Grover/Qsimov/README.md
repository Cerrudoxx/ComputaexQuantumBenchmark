# Grover's Algorithm Simulation with Qsimov

This application implements Grover's algorithm using the **Qsimov** library for quantum simulation. It measures execution time and standard deviation across multiple runs, monitors CPU and RAM usage, saves results to CSV files, and generates plots of RAM usage and execution times as a function of the number of qubits and iterations. The console output is enhanced using the **Rich** library for improved visualization.

## Requirements and Dependencies

To run this application, you need to install the following dependencies with the specified versions:

- **Python**: 3.8.20
- **psutil**: 7.0.0
- **numpy**: 1.24.4
- **matplotlib**: 3.5.1
- **rich**: (version not specified, but required for enhanced console output)
- **qsimov**: 5.1.3

Ensure you use compatible versions to avoid dependency conflicts.

## Installation

1. **Clone the repository** (if applicable) or download the files to your working directory.
2. **Install the dependencies**:
    - Use `pip` to install them manually:
      ```bash
      pip install psutil==5.9.0 numpy==2.0.2 qsimov matplotlib==3.5.0 rich
      ```
    - If a `requirements.txt` file exists, you can use:
      ```bash
      pip install -r requirements.txt
      ```

## Usage

The application is executed from the command line using the main script (`grover_qsimov_main.py`) and accepts the following arguments:

- `n`: Number of qubits or range of qubits (e.g., '4' or '4-7'). Must be greater than 2.
- `num_iterations`: Number of iterations or range of iterations (e.g., '512' or '512-1024'). Must be non-zero.
- `--cores`: Number of CPU cores to use (defaults to -1, which uses all available cores).
- `--no-ram`: Disables real-time RAM monitoring.
- `--no-cpu`: Disables CPU monitoring.

### Execution Examples

Run with 4 qubits, 512 iterations, and all available cores:
```bash
python grover_qsimov_main.py 4 512
```

Run with a qubit range from 4 to 7, iterations from 512 to 1024, and 2 cores:
```bash
python grover_qsimov_main.py 4-7 512-1024 --cores 2
```

Run with 5 qubits, 512 iterations, and no RAM monitoring:
```bash
python grover_qsimov_main.py 5 512 --no-ram
```

## Description of Main Classes and Modules

### GroverRunner (`grover_runner.py`)

- **Purpose**: Constructs and executes the quantum circuit for Grover's algorithm using Qsimov's `QCircuit` and `Drewom` executor, measuring its performance.
- **Input Parameters**:
  - `n`: Number of qubits.
  - `num_iterations`: Number of iterations for the simulation.
  - `cores`: Number of CPU cores.
  - `ram_monitor`: Instance of `RAMMonitor` (or `None` if not used).
  - `cpu_monitor`: Instance of `CPUMonitor` (or `None` if not used).
  - `console`: `Console` object from Rich for output.
  - `ram_csv_file`: Path to the CSV file for saving real-time RAM usage.
- **Key Methods**:
  - `_build_circuit()`: Constructs the Grover circuit with the optimal number of iterations using Hadamard (`H`), Pauli-X (`X`), and controlled-Z (`Z`) gates for the oracle and diffuser, followed by measurement.
  - `_run_simulation(num_executions)`: Runs the simulation multiple times using Qsimov's `Drewom` executor and returns execution times in nanoseconds.
  - `run()`: Executes the algorithm, calculates statistics (average time, standard deviation, CPU/RAM usage), and returns a dictionary with results. Stops execution if the estimated time exceeds one day (8640 seconds).

### ResultsHandler (`results_handler.py`)

- **Purpose**: Manages the visualization of results in tables and saves them to CSV files.
- **Input Parameters**:
  - `file_name`: Base name of the CSV file.
  - `results_dir`: Directory where results are saved.
  - `console`: `Console` object from Rich.
- **Key Methods**:
  - `_ensure_csv_headers()`: Ensures the CSV file has headers if it is new.
  - `save_to_csv(data)`: Appends data to the CSV file.
  - `display_timing_table(data)`: Displays a table with average execution time and standard deviation.
  - `display_usage_table(data)`: Displays a table with average CPU and RAM usage, RAM usage in MB, and peak RAM usage.
  - `save_console_output()`: Saves the console output to an `out.txt` file.

### CPUMonitor and RAMMonitor (`ResourceMonitor.py`)

- **Purpose**: Monitor CPU and RAM usage, respectively, during execution.
- **Input Parameters**:
  - `interval`: Sampling interval in seconds (default is 0.1).
- **Key Methods**:
  - `start()`: Starts monitoring in a separate thread.
  - `stop()`: Stops monitoring and joins the thread.
  - `average()`: Returns the average of the collected readings.
  - `max_memory_usage()` (only `RAMMonitor`): Returns the peak RAM usage as a percentage.
  - `memory_usage_in_mb()` (only `RAMMonitor`): Returns the current RAM usage in MB.
  - `max_memory_usage_in_mb()` (only `RAMMonitor`): Returns the peak RAM usage in MB.
  - `real_time_memory_usage(file_name)` (only `RAMMonitor`): Monitors and saves real-time RAM usage to a CSV file.
  - `plot_ram_usage_from_csv(file_name)`: Generates a plot of RAM usage over time from a CSV file.
  - `plot_ram_avg_from_results(file_name)`: Generates a plot of average RAM usage vs. number of qubits.
  - `plot_t_grover_from_csv(file_name)`: Generates a plot of Grover's execution time vs. number of qubits.

### Main Script (`grover_qsimov_main.py`)

- **Purpose**: Orchestrates the application's execution, parsing arguments, configuring resources, and coordinating classes.
- **Key Functions**:
  - `main()`: Parses command-line arguments, sets up the results directory, configures CPU cores, and runs the algorithm for each combination of qubits and iterations. It also initializes monitors, saves results, and generates plots.
- **Features**:
  - Supports ranges for qubits and iterations.
  - Creates unique result directories to avoid overwriting (e.g., `results_4_qubits_512_iterations_2_cores`).
  - Validates input arguments to ensure qubits are greater than 2 and iterations are non-zero.
  - Defaults to all available cores if `--cores` is set to -1.

## Application Flow

1. **Argument Parsing**: Reads command-line arguments (`n`, `num_iterations`, `--cores`, `--no-ram`, `--no-cpu`).
2. **Results Directory Creation**: Generates a unique directory based on the number of qubits, iterations, and cores.
3. **Core Configuration**: Limits the number of CPU cores to the available count or uses all cores if set to -1.
4. **Execution for Each `n` and `num_iterations`**:
   - Initializes `CPUMonitor` and `RAMMonitor` (if enabled).
   - Creates a `GroverRunner` instance to execute the algorithm.
   - Collects timing and resource usage statistics.
   - Uses `ResultsHandler` to display tables and save data to CSV.
5. **Plot Generation**: Creates plots for real-time RAM usage, average RAM usage vs. number of qubits, and Grover's execution time vs. number of qubits.
6. **Completion**: Saves the console output to `out.txt`.

## Output Files

- **Results CSV** (`Grover_data_qsimov_<n>.csv`): Contains execution data (number of qubits, iterations, Grover's time, standard deviation, CPU/RAM usage, etc.).
- **Real-Time RAM CSV** (`ram_usage_n<n>.csv`): Logs RAM usage in MB over time.
- **Plots**:
  - `ram_usage_n<n>.png`: Plot of real-time RAM usage over time.
  - `Grover_data_qsimov_<n>_ram_avg_qubits.png`: Plot of average RAM usage vs. number of qubits.
  - `Grover_data_qsimov_<n>_t_grover_qubits.png`: Plot of Grover's execution time vs. number of qubits.
- **Console Output** (`out.txt`): Log of all console output.

## Notes

- Real-time RAM monitoring is commented out in the main script (`grover_qsimov_main.py`). To enable it, uncomment the relevant lines in the `main()` function.
- The application automatically stops if the estimated execution time exceeds one day (`t_grover > 8640` seconds).
- Ensure the results directory does not already exist, as the script generates a new one with a unique name.
- The `plot_ram_usage_from_csv` function in `ResourceMonitor.py` may encounter issues with time parsing due to the format used in `real_time_memory_usage`. Consider updating the time format or error handling for robustness.
- The `qsimov` library uses a custom quantum machine (`Drewom`) with configurable threads, which is optimized for parallel execution based on the specified number of cores.

