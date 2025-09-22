import psutil
import sys
import time

def get_average_memory_usage(pid, interval=0.1):
    """Mide el uso de memoria de un proceso y sus subprocesos en MB y calcula el promedio."""
    try:
        # Obtener proceso principal
        main_process = psutil.Process(pid)
        memory_usages = []
        start_time = time.time()

        while psutil.pid_exists(pid):
            try:
                # Obtener procesos hijos (subprocesos de make)
                processes = [main_process] + main_process.children(recursive=True)
                total_memory_mb = 0
                for proc in processes:
                    try:
                        memory_info = proc.memory_info()
                        total_memory_mb += memory_info.rss / 1024 / 1024  # Convertir bytes a MB
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                memory_usages.append(total_memory_mb)
                time.sleep(interval)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break

        # Calcular promedio
        if memory_usages:
            avg_memory = sum(memory_usages) / len(memory_usages)
        else:
            avg_memory = 0
        return avg_memory
    except psutil.NoSuchProcess:
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 monitor_ram.py <pid>", file=sys.stderr)
        sys.exit(1)
    pid = int(sys.argv[1])
    avg_memory = get_average_memory_usage(pid)
    print(f"{avg_memory:.3f}")