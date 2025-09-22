#!/bin/bash

# Guardar toda la salida en un fichero OUT-[FECHAYHORA]
FECHA_HORA=$(date +"%Y%m%d-%H%M%S")
exec > >(tee "OUT-$FECHA_HORA") 2>&1
# Número de iteraciones
ITERATIONS=20 # Cambia este valor según necesites(este es el limite por arriba del rango de qubits a ejecutar)

COMPILATION_FILE="../build/compilation_stats.csv"

sed -i '2,$d' "$COMPILATION_FILE"

CONDA_ENV="Qiskit3"  # Cambia por el nombre de tu entorno conda

# Verificar si conda está disponible
if ! command -v conda &> /dev/null; then
    echo "Error: conda no está instalado o no se encuentra en el PATH."
    exit 1
fi



function execIterations(){

    for((j=1; j<=$INITIAL_ITERATIONS; j++)); do

    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$CONDA_ENV" || {
        echo "Error: No se pudo activar el entorno conda $CONDA_ENV."
        exit 1
    }

  
    if [ -f "generadorCircuitoGrover.py" ]; then
        python generadorCircuitoGrover.py "$i" || {
            echo "Error: Fallo al ejecutar generadorCircuitoGrover.py."
            exit 1
        }
    else
        echo "Error: El archivo generadorCircuitoGrover.py no se encuentra."
        exit 1
    fi


    cd ../build || {
        echo "Error: No se pudo cambiar al directorio ../build."
        exit 1
    }

    if [ -f "./scriptcompilacion.sh" ]; then
        bash ./scriptcompilacion.sh || {
            echo "Error: Fallo al ejecutar scriptcompilacion.sh."
            exit 1
        }
    else
        echo "Error: El archivo scriptcompilacion.sh no se encuentra."
        exit 1
    fi

    conda deactivate

    cd ../examples || {
        echo "Error: No se pudo cambiar al directorio ../examples."
        exit 1
    }

    if [ -f "./circuito.sh" ]; then
        bash ./circuito.sh || {
            echo "Error: Fallo al ejecutar ./circuito.sh."
            exit 1
        }
    else
        echo "Error: El archivo ./circuito.sh no se encuentra."
        exit 1
    fi
    done

}

# Bucle de iteraciones
for ((i=15; i<=ITERATIONS; i++)); do
    RESULTADOS_FILE="./Resultados/resultadosEjecucionQV${i}_qubit_.csv"
    INITIAL_ITERATIONS=10
    echo "Ejecutando iteración con $i qubits"

    execIterations

    conda activate "$CONDA_ENV" || {
        echo "Error: No se pudo activar el entorno conda $CONDA_ENV."
        exit 1
    }

    if [ -f "calculate_stats.py" ]; then
        OPTIMAL_ITERATIONS=$(python calculate_stats.py "$RESULTADOS_FILE" "$COMPILATION_FILE" "$i" 2> /dev/null) || {
            echo "Error: Fallo al ejecutar calculate_stats.py."
            exit 1
        }
        echo "--------------------------------------------------------------------------------"
        echo "Número óptimo de iteraciones para $i qubits: $OPTIMAL_ITERATIONS"
        echo "--------------------------------------------------------------------------------"
    else
        echo "Error: El archivo calculate_stats.py no se encuentra."
        exit 1
    fi

    INITIAL_ITERATIONS=$((OPTIMAL_ITERATIONS - 10))

    conda deactivate

    execIterations
    
    conda activate "$CONDA_ENV" || {
        echo "Error: No se pudo activar el entorno conda $CONDA_ENV."
        exit 1
    }

    if [ -f "calculate_final_stats.py" ]; then
        read MEAN_RESULTADOS STD_RESULTADOS MEAN_COMPILATION STD_COMPILATION MEAN_COMBINED STD_COMBINED MEAN_RAM_RESULTS MEAN_RAM_COMPILATION< <(python calculate_final_stats.py "$RESULTADOS_FILE" "$COMPILATION_FILE" "$i" 2> /dev/null) || {
            echo "Error: Fallo al ejecutar calculate_final_stats.py."
            exit 1
        }
        echo "Estadísticas finales para $i qubits:"
        echo "Resultados - Media: $MEAN_RESULTADOS s, Desviación estándar: $STD_RESULTADOS s"
        echo "Compilación - Media: $MEAN_COMPILATION s, Desviación estándar: $STD_COMPILATION s"
        echo "Combinado - Media: $MEAN_COMBINED s, Desviación estándar: $STD_COMBINED s"
        echo "Consumo de Memoria - Ejecución: $MEAN_RAM_RESULTS MB, Compilación: $MEAN_RAM_COMPILATION MB"
    else
        echo "Error: El archivo calculate_final_stats.py no se encuentra."
        exit 1
    fi

    conda deactivate

    sed -i '2,$d' "$COMPILATION_FILE"
    #echo "" >> "$COMPILATION_FILE"

    echo "Iteración $i completada."
done

conda deactivate

echo "Todas las iteraciones completadas exitosamente."