# Grover's Algorithm Simulation with Qulacs

This application implements Grover's algorithm using the **Qulacs** library for quantum simulation. In addition to running the algorithm, it measures execution time and standard deviation across multiple runs, monitors CPU and RAM usage, saves results to CSV files, and generates plots of RAM usage and execution times as a function of the number of qubits. The console output is enhanced using the **Rich** library.

## Requirements and Dependencies

To run this application, you need to install the following dependencies with the specified versions:

- **Python**: 3.9.21
- **psutil**: 5.9.0
- **numpy**: 2.0.2
- **matplotlib**: 3.5.0
- **rich**: (version not specified, but required for enhanced console output)

Ensure you use these versions to guarantee compatibility.

## Installation

1. **Clone the repository** (if applicable) or download the files to your working directory.
2. **Install the dependencies**:
    - Use `pip` to install them manually:
      ```bash
      pip install psutil==5.9.0 numpy==2.0.2 qulacs==0.6.11 matplotlib==3.5.0 rich
      ```
    - If a `requirements.txt` file exists, you can use:
      ```bash
      pip install -r requirements.txt
      ```

## Usage

The application is executed from the command line using the main script (`grover_qulacs_main.py`) and accepts the following arguments:

- `n`: Number of qubits or range of qubits (e.g., '4' or '4-7'). Must be greater than 2.
- `--cores`: Number of CPU cores to use (defaults to all available cores).
- `--no-ram`: Disables RAM monitoring.
- `--no-cpu`: Disables CPU monitoring.

### Execution Examples

Run with 4 qubits and all available cores:
```bash
python grover_qulacs_main.py 4
```

Run with a qubit range from 4 to 7 and 2 cores:
```bash
python grover_qulacs_main.py 4-7 --cores 2
```

Run with 5 qubits without RAM monitoring:
```bash
python grover_qulacs_main.py 5 --no-ram
```

## Description of Main Classes

### GroverRunner (`grover_runner.py`)

- **Purpose**: Builds and executes the quantum circuit for Grover's algorithm, measuring its performance.
- **Input Parameters**:
  - `n`: Number of qubits.
  - `cores`: Number of CPU cores.
  - `ram_monitor`: Instance of `RAMMonitor` (or `None` if not used).
  - `cpu_monitor`: Instance of `CPUMonitor` (or `None` if not used).
  - `console`: `Console` object from Rich for output.
  - `ram_csv_file`: Path to the CSV file for saving real-time RAM usage.
- **Key Methods**:
  - `_build_circuit()`: Constructs the Grover circuit with the optimal number of iterations.
  - `_run_simulation(num_iterations)`: Runs the simulation multiple times and returns times in nanoseconds.
  - `run()`: Executes the algorithm, calculates statistics (average time, standard deviation, CPU/RAM usage), and returns a dictionary with the results.

### ResultsHandler (`results_handler.py`)

- **Purpose**: Handles the visualization of results in tables and saves them to CSV files.
- **Input Parameters**:
  - `file_name`: Base name of the CSV file.
  - `results_dir`: Directory where results are saved.
  - `console`: `Console` object from Rich.
- **Key Methods**:
  - `save_to_csv(data)`: Saves data to a CSV file.
  - `display_timing_table(data)`: Displays a table with average time and standard deviation.
  - `display_usage_table(data)`: Displays a table with average CPU and RAM usage.
  - `save_console_output()`: Saves the console output to an `out.txt` file.

### CPUMonitor and RAMMonitor (`ResourceMonitor.py`)

- **Purpose**: Monitor CPU and RAM usage, respectively, during execution.
- **Input Parameters**:
  - `interval`: Sampling interval in seconds (default is 0.1).
- **Key Methods**:
  - `start()`: Starts monitoring in a separate thread.
  - `stop()`: Stops monitoring.
  - `average()`: Returns the average of the readings.
  - `max_memory_usage()` (only `RAMMonitor`): Returns the peak RAM usage.
  - `memory_usage_in_mb()` (only `RAMMonitor`): Returns RAM usage in MB.
  - `real_time_memory_usage(file_name)` (only `RAMMonitor`): Monitors anda21:21:21 10:9:9 AM CST
- `real_time_memory_usage(file_name)` (only `RAMMonitor`): Monitors and saves real-time RAM usage to a CSV file.
- `plot_ram_usage_from_csv(file_name)`: Generates a plot of RAM usage from a CSV file.
- `plot_ram_avg_from_results(file_name)`: Generates a plot of average RAM usage vs. number of qubits.
- `plot_t_grover_from_csv(file_name)`: Generates a plot of Grover's time vs. number of qubits.

### Main Script (`grover_qulacs_main.py`)

- **Purpose**: Orchestrates the application's execution, configuring cores, handling arguments, and coordinating classes.
- **Key Functions**:
  - `set_active_cores(cores)`: Configures the number of active cores using environment variables and CPU affinity.
  - `main()`: Parses arguments, sets up the environment, runs the algorithm for each number of qubits, and saves the results.

## Application Flow

1. **Argument Parsing**: Reads command-line arguments (`n`, `--cores`, `--no-ram`, `--no-cpu`).
2. **Core Configuration**: Adjusts the CPU cores to use with `set_active_cores()`.
3. **Results Directory Creation**: Generates a unique directory (e.g., `results_4_qubits_2_cores`) to store data.
4. **Execution for Each `n`**:
   - Creates an instance of `GroverRunner` and runs the algorithm.
   - Collects timing and resource usage statistics.
   - Uses `ResultsHandler` to display tables and save data to CSV.
5. **Plot Generation**: Creates plots for real-time RAM usage, average RAM usage, and Grover's time vs. number of qubits.
6. **Completion**: Saves the console output to `out.txt`.

## Output Files

- **Results CSV** (`Grover_data_qulacs_<n>.csv`): Contains execution data (number of qubits, iterations, Grover's time, standard deviation, CPU/RAM usage, etc.).
- **Real-Time RAM CSV** (`ram_usage_n<n>.csv`): Logs RAM usage in MB over time.
- **Plots**:
  - `ram_usage_n<n>.png`: Plot of real-time RAM usage.
  - `Grover_data_qulacs_<n>_ram_avg_qubits.png`: Plot of average RAM usage vs. number of qubits.
  - `Grover_data_qulacs_<n>_t_grover_qubits.png`: Plot of Grover's time vs. number of qubits.
- **Console Output** (`out.txt`): Log of all console output.

## Notes

- Real-time RAM monitoring is currently commented out in the code (`grover_qulacs_main.py`). To enable it, uncomment the relevant lines in the `main()` function.
- If the estimated execution time exceeds one day (`t_grover > 8640` seconds), the program stops automatically.
- Ensure the results directory does not already exist, as the script generates a new one with a unique name.

