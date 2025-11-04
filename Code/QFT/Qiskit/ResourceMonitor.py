import threading
import time
import psutil
import csv
import os
import matplotlib.pyplot as plt
import rich
from rich.console import Console
from matplotlib.ticker import MaxNLocator
import matplotlib
import datetime


console = Console()

class CPUMonitor:
    """A class to monitor CPU usage in a separate thread.

    Attributes:
        interval (float): The interval in seconds at which to sample CPU usage.
        readings (list): A list of CPU usage readings.
    """
    def __init__(self, interval=0.1):
        """Initializes the CPUMonitor.

        Args:
            interval (float, optional): The interval in seconds at which to sample CPU usage.
                Defaults to 0.1.
        """
        self.interval = interval
        self.readings = []
        self._monitoring = False

    def _monitor(self):
        """Continuously monitors CPU usage and records readings."""
        while self._monitoring:
            self.readings.append(psutil.cpu_percent(interval=None))
            time.sleep(self.interval)

    def start(self):
        """Starts the CPU monitoring thread."""
        self._monitoring = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stops the CPU monitoring thread."""
        self._monitoring = False
        self.thread.join()

    def average(self):
        """Calculates the average CPU usage.

        Returns:
            float: The average CPU usage, or 0.0 if no readings were taken.
        """
        return sum(self.readings) / len(self.readings) if self.readings else 0.0

class RAMMonitor:
    """A class to monitor RAM usage in a separate thread.

    Attributes:
        interval (float): The interval in seconds at which to sample RAM usage.
        readings (list): A list of RAM usage readings.
    """
    def __init__(self, interval=0.1):
        """Initializes the RAMMonitor.

        Args:
            interval (float, optional): The interval in seconds at which to sample RAM usage.
                Defaults to 0.1.
        """
        self.interval = interval
        self.readings = []
        self._monitoring = False

    def _monitor(self):
        """Continuously monitors RAM usage and records readings."""
        process = psutil.Process()
        while self._monitoring:
            self.readings.append(process.memory_percent())
            time.sleep(self.interval)

    def start(self):
        """Starts the RAM monitoring thread."""
        self._monitoring = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stops the RAM monitoring thread."""
        self._monitoring = False
        self.thread.join()

    def average(self):
        """Calculates the average RAM usage.

        Returns:
            float: The average RAM usage, or 0.0 if no readings were taken.
        """
        return sum(self.readings) / len(self.readings) if self.readings else 0.0
            
    def max_memory_usage(self):
        """Calculates the maximum RAM usage.

        Returns:
            float: The maximum RAM usage, or 0.0 if no readings were taken.
        """
        return max(self.readings) if self.readings else 0.0

    def memory_usage_in_mb(self):
        """Gets the current RAM usage in megabytes.

        Returns:
            float: The current RAM usage in megabytes.
        """
        process = psutil.Process()
        memory_info = process.memory_info()
        return memory_info.rss / (1024 * 1024)

    def max_memory_usage_in_mb(self):
        """Calculates the maximum RAM usage in megabytes.

        Returns:
            float: The maximum RAM usage in megabytes, or 0.0 if no readings were taken.
        """
        return max(self.readings) * psutil.virtual_memory().total / (1024 * 1024 * 100) if self.readings else 0.0
    
    
    def real_time_memory_usage(self, file_name):
        """Records real-time memory usage to a CSV file.

        Args:
            file_name (str): The name of the CSV file to write to.
        """
        process = psutil.Process()
        if not os.path.isfile(file_name):
            with open(file_name, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Time', 'RAM Usage (MB)'])
        
        with open(file_name, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            start_time = time.perf_counter()
            while self._monitoring:
                elapsed = time.perf_counter() - start_time
                mem_usage = process.memory_info().rss / (1024 * 1024)
                current_time = f"{elapsed:.3f}"
                csv_writer.writerow([current_time, mem_usage])
                csv_file.flush()
                next_time = elapsed + self.interval
                time.sleep(max(0, next_time - (time.perf_counter() - start_time)))

def create_ram_usage_csv(file_name, time, ram_usage):
    """Appends a timestamp and RAM usage to a CSV file.

    Args:
        file_name (str): The name of the CSV file.
        time (str): The timestamp to record.
        ram_usage (float): The RAM usage to record.
    """
    file_exists = os.path.isfile(file_name)
    with open(file_name, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if not file_exists:
            csv_writer.writerow(['Time', 'RAM Usage (MB)'])
        csv_writer.writerow([time, ram_usage])
        
def plot_ram_usage_from_csv(file_name):
    """Creates a plot of RAM usage over time from a CSV file.

    Args:
        file_name (str): The name of the CSV file.
    """
    print(file_name)
    times = []
    ram_usages = []
    
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        start_time = None
        for row in csv_reader:
            try:
                current_time = time.strptime(row[0], "%H:%M:%S")
                if start_time is None:
                    start_time = current_time
                elapsed_time = time.mktime(current_time) - time.mktime(start_time)
                times.append(elapsed_time)
                ram_usages.append(float(row[1]))
            except ValueError as e:
                console.print(f"Skipping row due to error: {e}", style="bold red")
    
    if len(times) > 1 and len(ram_usages) > 1:
        plt.figure(figsize=(10, 5))
        plt.plot(times, ram_usages, linestyle='-', color='b', marker='o')
        plt.xlabel('Elapsed Time (seconds)')
        plt.ylabel('RAM Usage (MB)')
        plt.title('RAM Usage Over Time')
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.tight_layout()
        
        png_file_name = file_name.replace('.csv', '.png')
        plt.savefig(png_file_name)
        console.print(f"Graph saved as {png_file_name}", style="bold green")
    else:
        console.print("Not enough data to plot.", style="bold red")

def plot_ram_avg_from_results(file_name):
    """Creates a plot of average RAM usage vs. number of qubits from a CSV file.

    Args:
        file_name (str): The name of the CSV file.
    """
    try:
        qubits = []
        ram_mb = []
        
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                qubits.append(int(row[0]))
                ram_mb.append(float(row[6]))
        
        if qubits and ram_mb:
            plt.figure(figsize=(10, 5))
            plt.plot(qubits, ram_mb, linestyle='-', color='g', marker='o')
            plt.xlabel('Number of Qubits')
            plt.ylabel('RAM Average Usage (MB)')
            plt.title('RAM Average Usage vs Number of Qubits')
            plt.grid(True)
            plt.tight_layout()
            
            png_file_name = file_name.replace('.csv', '_ram_avg_qubits.png')
            plt.savefig(png_file_name)
            console.print(f"Graph saved as {png_file_name}", style="bold green")
        else:
            console.print("No data available to plot.", style="bold red")
    except Exception as e:
        console.print(f"Error while processing the file: {e}", style="bold red")
        
def plot_t_grover_from_csv(file_name):
    """Creates a plot of execution time vs. number of qubits from a CSV file.

    Args:
        file_name (str): The name of the CSV file.
    """
    try:
        n_values = []
        t_grover_values = []
        
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                n_values.append(int(row[0]))
                t_grover_values.append(float(row[2]))
        
        if n_values and t_grover_values:
            plt.figure(figsize=(10, 5))
            plt.plot(n_values, t_grover_values, linestyle='-', color='r', marker='o')
            plt.xlabel('Number of Qubits')
            plt.ylabel('Grover Time (s)')
            plt.title('Grover Time vs Number of Qubits')
            plt.grid(True)
            plt.tight_layout()
            
            png_file_name = file_name.replace('.csv', '_t_grover_qubits.png')
            plt.savefig(png_file_name)
            console.print(f"Graph saved as {png_file_name}", style="bold green")
        else:
            console.print("No data available to plot.", style="bold red")
    except Exception as e:
        console.print(f"Error while processing the file: {e}", style="bold red")       