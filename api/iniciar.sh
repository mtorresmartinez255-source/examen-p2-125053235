#!/bin/sh
set -e

echo "Esperando resultados de Hadoop..."

while [ ! -f /app/resultados/resultado/_SUCCESS ] || \
      [ ! -s /app/resultados/resultado/part-00000 ]; do
    sleep 2
done

echo "Resultados de Hadoop disponibles."

python /app/scripts/cargar_resultados.py

echo "Iniciando API Flask..."

exec python /app/app.py
