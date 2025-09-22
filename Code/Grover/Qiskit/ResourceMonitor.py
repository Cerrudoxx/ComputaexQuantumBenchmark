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
    def __init__(self, interval=0.1):
        self.interval = interval
        self.readings = []
        self._monitoring = False

    def _monitor(self):
        while self._monitoring:
            self.readings.append(psutil.cpu_percent(interval=None))
            time.sleep(self.interval)

    def start(self):
        self._monitoring = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self._monitoring = False
        self.thread.join()

    def average(self):
        return sum(self.readings) / len(self.readings) if self.readings else 0.0

class RAMMonitor:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.readings = []
        self._monitoring = False

    def _monitor(self):
        process = psutil.Process()
        while self._monitoring:
            self.readings.append(process.memory_percent())
            time.sleep(self.interval)

    def start(self):
        self._monitoring = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self._monitoring = False
        self.thread.join()

    def average(self):
        #print("Readings for the memory avg", self.readings)
        return sum(self.readings) / len(self.readings) if self.readings else 0.0
            
    def max_memory_usage(self):
        return max(self.readings) if self.readings else 0.0

    def memory_usage_in_mb(self):
        process = psutil.Process()
        memory_info = process.memory_info()
        return memory_info.rss / (1024 * 1024)  # Convertir bytes a MB

    def max_memory_usage_in_mb(self):
        return max(self.readings) * psutil.virtual_memory().total / (1024 * 1024 * 100) if self.readings else 0.0
    
    
    def real_time_memory_usage(self, file_name):
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
                current_time = f"{elapsed:.3f}"  # Tiempo relativo en segundos
                csv_writer.writerow([current_time, mem_usage])
                csv_file.flush()
                next_time = elapsed + self.interval
                time.sleep(max(0, next_time - (time.perf_counter() - start_time)))

def create_ram_usage_csv(file_name, time, ram_usage):

    file_exists = os.path.isfile(file_name)
    with open(file_name, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if not file_exists:
            csv_writer.writerow(['Time', 'RAM Usage (MB)'])
        csv_writer.writerow([time, ram_usage])
        
def plot_ram_usage_from_csv(file_name):
    """
    Crea una gráfica a partir del contenido de un archivo CSV que contiene el uso de RAM.
    
    Parámetros:
    file_name: str - Nombre del archivo CSV.
    """
    print(file_name)
    times = []
    ram_usages = []
    
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header
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
        plt.plot(times, ram_usages, linestyle='-', color='b', marker='o')  # Add marker='o' back
        plt.xlabel('Elapsed Time (seconds)')
        plt.ylabel('RAM Usage (MB)')
        plt.title('RAM Usage Over Time')
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))  # Limita a 10 etiquetas
        plt.tight_layout()
        
        # Guardar la gráfica como una imagen PNG
        png_file_name = file_name.replace('.csv', '.png')
        plt.savefig(png_file_name)
        console.print(f"Graph saved as {png_file_name}", style="bold green")
    else:
        console.print("Not enough data to plot.", style="bold red")

def plot_ram_avg_from_results(file_name):
    """
    Crea una gráfica a partir del contenido de un archivo CSV que contiene el promedio de uso de RAM,
    comparándolo con el número de qubits.
    
    Parámetros:
    file_name: str - Nombre del archivo CSV.
    """
    try:
        qubits = []
        ram_mb = []
        
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                qubits.append(int(row[0]))  # number_of_qubits
                ram_mb.append(float(row[6]))  # ram_avg
        
        if qubits and ram_mb:
            plt.figure(figsize=(10, 5))
            plt.plot(qubits, ram_mb, linestyle='-', color='g', marker='o')
            plt.xlabel('Number of Qubits')
            plt.ylabel('RAM Average Usage (MB)')
            plt.title('RAM Average Usage vs Number of Qubits')
            plt.grid(True)
            plt.tight_layout()
            
            # Guardar la gráfica como una imagen PNG
            png_file_name = file_name.replace('.csv', '_ram_avg_qubits.png')
            plt.savefig(png_file_name)
            console.print(f"Graph saved as {png_file_name}", style="bold green")
        else:
            console.print("No data available to plot.", style="bold red")
    except Exception as e:
        console.print(f"Error while processing the file: {e}", style="bold red")
        
def plot_t_grover_from_csv(file_name):
    """
    Crea una gráfica a partir del contenido de un archivo CSV que contiene los tiempos de Grover.
    
    Parámetros:
    file_name: str - Nombre
    """
    try:
        n_values = []
        t_grover_values = []
        
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                n_values.append(int(row[0]))  # number_of_qubits
                t_grover_values.append(float(row[2]))  # t_grover
        
        if n_values and t_grover_values:
            plt.figure(figsize=(10, 5))
            plt.plot(n_values, t_grover_values, linestyle='-', color='r', marker='o')
            plt.xlabel('Number of Qubits')
            plt.ylabel('Grover Time (s)')
            plt.title('Grover Time vs Number of Qubits')
            plt.grid(True)
            plt.tight_layout()
            
            # Guardar la gráfica como una imagen PNG
            png_file_name = file_name.replace('.csv', '_t_grover_qubits.png')
            plt.savefig(png_file_name)
            console.print(f"Graph saved as {png_file_name}", style="bold green")
        else:
            console.print("No data available to plot.", style="bold red")
    except Exception as e:
        console.print(f"Error while processing the file: {e}", style="bold red")       