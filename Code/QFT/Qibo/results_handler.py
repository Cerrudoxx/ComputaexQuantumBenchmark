import os
import csv
from rich.console import Console
from rich.table import Table
from datetime import datetime

class ResultsHandler:
    """A class to handle the display and saving of results.

    Attributes:
        file_name (str): The name of the CSV file to save results to.
        results_dir (str): The directory to save results in.
        console (Console): The rich console object to use for output.
    """
    
    def __init__(self, file_name: str, results_dir: str, console: Console):
        """Initializes the ResultsHandler.

        Args:
            file_name (str): The name of the CSV file to save results to.
            results_dir (str): The directory to save results in.
            console (Console): The rich console object to use for output.
        """
        self.file_name = os.path.join(results_dir, file_name + '.csv')
        self.results_dir = results_dir
        self.console = console
        self._ensure_csv_headers()

    def _ensure_csv_headers(self) -> None:
        """Ensures that the CSV file has headers if it is new."""
        if not os.path.isfile(self.file_name):
            with open(self.file_name, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['n', 'iterations_number', 't_grover', 'std_grover', 
                                   'cpu_avg', 'ram_avg', 'ram_mb', 'ram_peak','cores'])

    def save_to_csv(self, data: dict) -> None:
        """Saves the given data to the CSV file.

        Args:
            data (dict): A dictionary containing the data to save.
        """
        with open(self.file_name, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([data['n'], data['iterations_number'], data['t_grover'], 
                               data['std_grover'], data['cpu_avg'], data['ram_avg'], 
                               data['ram_mb'], data['max_ram_peak'], data['cores']])
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.console.print(f"Data appended to {self.file_name} at {current_time}", style="bold red")

    def display_timing_table(self, data: dict) -> None:
        """Displays a table of timing and deviation data.

        Args:
            data (dict): A dictionary containing the timing data.
        """
        table = Table(title="Tiempo y Desviación")
        table.add_column("Tiempo Medio Total (s)", justify="center", style="cyan")
        table.add_column("Desviación Típica (s)", justify="center", style="magenta")
        table.add_row(f"{data['t_grover']:.6f}", f"{data['std_grover']:.6f}")
        self.console.print(table)

    def display_usage_table(self, data: dict) -> None:
        """Displays a table of CPU and RAM usage data.

        Args:
            data (dict): A dictionary containing the usage data.
        """
        table = Table(title="Uso de CPU y RAM")
        table.add_column("CPU Avg (%)", justify="center", style="green")
        table.add_column("RAM Avg (%)", justify="center", style="red")
        table.add_column("RAM Usage (MB)", justify="center", style="blue")
        table.add_column("Max RAM Peak (%)", justify="center", style="yellow")
        table.add_row(f"{data['cpu_avg']:.2f}", f"{data['ram_avg']:.2f}", 
                     f"{data['ram_mb']:.2f}", f"{data['max_ram_peak']:.2f}")
        self.console.print(table)

    def save_console_output(self) -> None:
        """Saves the console output to a file."""
        with open(os.path.join(self.results_dir, "out.txt"), "w") as f:
            f.write(self.console.export_text())