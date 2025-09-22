#!/bin/bash

# Forzar la localización a C para usar punto decimal
export LC_NUMERIC=C

# Archivo CSV para almacenar resultados
CSV_FILE="compilation_stats.csv"

# Crear archivo CSV con encabezados si no existe
if [ ! -f "$CSV_FILE" ]; then
    echo "Timestamp,Command,Duration_ms,Average_RAM_MB" > "$CSV_FILE"
fi

# Obtener timestamp actual
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Obtener tiempo inicial en nanosegundos
start=$(date +%s.%N)

# Ejecutar make -j17 y obtener su PID
make -j17 &
MAKE_PID=$!


# Monitorear uso de RAM con script en Python
RAM_SCRIPT="monitor_ram.py"
if [ ! -f "$RAM_SCRIPT" ]; then
    echo "Error: Script $RAM_SCRIPT no encontrado."
    exit 1
fi
avg_ram=$(python3 "$RAM_SCRIPT" $MAKE_PID)

# Verificar si make falló
wait $MAKE_PID
if [ $? -ne 0 ]; then
    echo "Error: Fallo en la compilación."
    exit 1
fi

# Obtener tiempo final en nanosegundos
end=$(date +%s.%N)

# Calcular duración en milisegundos con 6 decimales de precisión
duration=$(echo "scale=6; ($end - $start) * 1000" | bc)

# Imprimir resultado con 3 decimales
printf "Tiempo de compilación: %.3f milisegundos\n" "$duration"
printf "Uso medio de RAM: %.3f MB\n" "$avg_ram"

# Guardar resultados en CSV
echo "$timestamp,make -j17,$duration,$avg_ram" >> "$CSV_FILE"

exit 0