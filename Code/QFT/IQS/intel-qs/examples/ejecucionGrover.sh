#!/bin/bash

# Guardar toda la salida en un fichero OUT-[FECHAYHORA]
FECHA_HORA=$(date +"%Y%m%d-%H%M%S")
exec > >(tee "OUT-$FECHA_HORA") 2>&1
# Número de iteraciones
ITERATIONS=20 # Cambia este valor según necesites

# Nombre del entorno conda
CONDA_ENV="Qiskit3"  # Cambia por el nombre de tu entorno conda

# Verificar si conda está disponible
if ! command -v conda &> /dev/null; then
    echo "Error: conda no está instalado o no se encuentra en el PATH."
    exit 1
fi


# Bucle de iteraciones
for ((i=20; i<=ITERATIONS; i++)); do
    echo "Ejecutando iteración con $i qubits"

    # Activar el entorno conda
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$CONDA_ENV" || {
        echo "Error: No se pudo activar el entorno conda $CONDA_ENV."
        exit 1
    }

    # Ejecutar el script Python
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
    # Ejecutar el script de compilación
    if [ -f "./scriptcompilacion.sh" ]; then
        bash ./scriptcompilacion.sh || {
            echo "Error: Fallo al ejecutar scriptcompilacion.sh."
            exit 1
        }
    else
        echo "Error: El archivo scriptcompilacion.sh no se encuentra."
        exit 1
    fi

        # Desactivar el entorno conda antes de ejecutar los siguientes scripts
    conda deactivate

    cd ../examples || {
        echo "Error: No se pudo cambiar al directorio ../examples."
        exit 1
    }
    # Ejecutar el script circuito.sh
    if [ -f "./circuito.sh" ]; then
        bash ./circuito.sh || {
            echo "Error: Fallo al ejecutar ./circuito.sh."
            exit 1
        }
    else
        echo "Error: El archivo ./circuito.sh no se encuentra."
        exit 1
    fi

    echo "Iteración $i completada."
done

# Desactivar el entorno conda
conda deactivate

echo "Todas las iteraciones completadas exitosamente."