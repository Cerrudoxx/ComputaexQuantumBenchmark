#!/bin/bash

# Forzar la localización a C para usar punto decimal
export LC_NUMERIC=C

# Obtener tiempo inicial en nanosegundos
start=$(date +%s.%N)

# Ejecutar make -j17
make -j17 || {
    echo "Error: Fallo en la compilación."
    exit 1
}

# Obtener tiempo final en nanosegundos
end=$(date +%s.%N)

# Calcular duración en milisegundos con 6 decimales de precisión
duration=$(echo "scale=6; ($end - $start) * 1000" | bc)

# Imprimir resultado con 3 decimales
printf "Tiempo de compilación: %.3f milisegundos\n" "$duration"

exit 0