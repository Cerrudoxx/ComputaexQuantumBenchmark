import statistics
import pandas as pd
import sys

def calculate_final_stats(resultados_file, compilation_file, qubits):
    try:
        # Leer los archivos CSV
        resultados_df = pd.read_csv(resultados_file)
        compilation_df = pd.read_csv(compilation_file)
        
        # Extraer los tiempos de ejecución (en ms) del primer archivo
        tiempos_resultados = resultados_df['Tiempo promedio (ms)'].tolist()
        
        # Extraer los tiempos de ejecución (en ms) del segundo archivo
        tiempos_compilation = compilation_df['Duration_ms'].tolist()
        
        #Extraer la media de uso de memoria (en KB) del primer archivo
        memoria_media_resultados = resultados_df['RAM media (KB)'].tolist()
        
        memoria_media_compilation = compilation_df['Average_RAM_MB'].tolist()
        
        # Calcular media y desviación estándar para el primer archivo (en segundos)
        mean_resultados = statistics.mean(tiempos_resultados) / 1000 if tiempos_resultados else 0
        std_resultados = statistics.stdev(tiempos_resultados) / 1000 if len(tiempos_resultados) > 1 else 0
        
        # Calcular media y desviación estándar para el segundo archivo (en segundos)
        mean_compilation = statistics.mean(tiempos_compilation) / 1000 if tiempos_compilation else 0
        std_compilation = statistics.stdev(tiempos_compilation) / 1000 if len(tiempos_compilation) > 1 else 0
        
        #Calcula la media de uso de memoria (en KB)
        
        mean_memoria_resultados = statistics.mean(memoria_media_resultados) if memoria_media_resultados else 0
        mean_memoria_compilation = statistics.mean(memoria_media_compilation) if memoria_media_compilation else 0

        mean_memoria_resultados_mb = mean_memoria_resultados / 1024 if mean_memoria_resultados else 0
        mean_memoria_compilation_mb = mean_memoria_compilation / 1024 if mean_memoria_compilation else 0
            
        # Combinar los tiempos sumándolos elemento por elemento (mínimo de longitudes)
        min_length = min(len(tiempos_resultados), len(tiempos_compilation))
        combined_times = [tiempos_resultados[i] + tiempos_compilation[i] for i in range(min_length)]
        combined_times_seconds = [t / 1000 for t in combined_times]
        
        # Calcular media y desviación estándar para los tiempos combinados
        mean_combined = statistics.mean(combined_times_seconds) if combined_times_seconds else 0
        std_combined = statistics.stdev(combined_times_seconds) if len(combined_times_seconds) > 1 else 0
        

        combined_stats_df = pd.DataFrame({
            'Qubits': [qubits],
            'Mean_Combined_s': [mean_combined],
            'Std_Combined_s': [std_combined],
            'Mean_Compilation_s': [mean_compilation],
            'Std_Compilation_s': [std_compilation],
            'Mean_Resultados_s': [mean_resultados],
            'Std_Resultados_s': [std_resultados],
            'Mean_Memoria_Resultados_MB': [mean_memoria_resultados_mb],
            'Mean_Memoria_Compilation_MB': [mean_memoria_compilation_mb]
        })
        

        combined_stats_df.to_csv(f'./Resultados/combined_stats_QV{qubits}_qubit.csv', index=False)
        
        # Imprimir resultados para el script Bash (media y desviación estándar en segundos)
        print(f"{mean_resultados} {std_resultados} {mean_compilation} {std_compilation} {mean_combined} {std_combined} {mean_memoria_resultados_mb} {mean_memoria_compilation_mb}")
        
        # Imprimir resultados para depuración
        print(f"Estadísticas calculadas para {qubits} qubits:")
        print(f"Resultados - Media: {mean_resultados:.6f} s, Desviación estándar: {std_resultados:.6f} s")
        print(f"Compilación - Media: {mean_compilation:.6f} s, Desviación estándar: {std_compilation:.6f} s")
        print(f"Combinado - Media: {mean_combined:.6f} s, Desviación estándar: {std_combined:.6f} s")
        print(f"Memoria - Resultados: {mean_memoria_resultados_mb:.2f} MB, Compilación: {mean_memoria_compilation_mb:.2f} MB")
        
        return mean_resultados, std_resultados, mean_compilation, std_compilation, mean_combined, std_combined
    
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar uno de los archivos CSV: {e}", file=sys.stderr)
        exit(1)
    except Exception as e:
        print(f"Error al procesar los datos: {e}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python calculate_final_stats.py <resultados_file> <compilation_file> <qubits>", file=sys.stderr)
        sys.exit(1)
    
    resultados_file = sys.argv[1]
    compilation_file = sys.argv[2]
    qubits = int(sys.argv[3])
    
    calculate_final_stats(resultados_file, compilation_file, qubits)