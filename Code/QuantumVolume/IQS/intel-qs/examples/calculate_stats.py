
import statistics
import math
import pandas as pd
from datetime import datetime
from rich.console import Console

def calculate_stats(resultados_file, compilation_file, n_iterations_in):
    console = Console()
    
    try:
        # Leer los archivos CSV
        resultados_df = pd.read_csv(resultados_file)
        compilation_df = pd.read_csv(compilation_file)
        
        # Extraer los tiempos de ejecución (en ms) del primer archivo
        tiempos_resultados = resultados_df['Tiempo promedio (ms)'].tolist()
        
        # Extraer los tiempos de ejecución (en ms) del segundo archivo
        tiempos_compilation = compilation_df['Duration_ms'].tolist()
        
        # Combinar los tiempos sumándolos elemento por elemento
        # Asumimos que ambas listas tienen la misma longitud; si no, tomamos el mínimo
        min_length = min(len(tiempos_resultados), len(tiempos_compilation))
        combined_times = [tiempos_resultados[i] + tiempos_compilation[i] for i in range(min_length)]
        
        # Convertir tiempos combinados a segundos (de ms a s, dividiendo por 1000)
        combined_times_seconds = [t / 1000 for t in combined_times]
        
        # Calcular la media y la desviación estándar en segundos
        t_grover = statistics.mean(combined_times_seconds) if combined_times_seconds else 0
        std_grover = statistics.stdev(combined_times_seconds) if len(combined_times_seconds) > 1 else 0
        
        # Verificar si el tiempo excede 2.4 horas (8640 segundos)
        if t_grover > 8640:
            console.print(f"El algoritmo tarda más de un día en ejecutarse. Deteniendo la ejecución a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="red")
            exit(0)
        
        # Calcular el número óptimo de iteraciones
        iterations_number = (math.ceil((2 * 1.96 * std_grover) / (0.05 * t_grover)))**2 if t_grover > 0 else n_iterations_in
        #console.print(f"Optimal number of iterations: {iterations_number}", style="blue")
        
        print(iterations_number)
        return iterations_number
    
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar uno de los archivos CSV: {e}")
        exit(1)
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        exit(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Uso: python calculate_stats.py <resultados_file> <compilation_file> <n_iterations_in>")
        sys.exit(1)
    
    resultados_file = sys.argv[1]
    compilation_file = sys.argv[2]
    n_iterations_in = int(sys.argv[3])
    
    calculate_stats(resultados_file, compilation_file, n_iterations_in)