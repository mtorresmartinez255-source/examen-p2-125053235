#!/bin/bash
set -euo pipefail

ENTRADA="/data/input/ventas_125053235.csv"
SALIDA="/data/output/resultado"

if [ ! -f "$ENTRADA" ]; then
    echo "ERROR: No existe el dataset $ENTRADA"
    exit 1
fi

mkdir -p /data/output

if [ -d "$SALIDA" ]; then
    rm -rf "$SALIDA"
fi

echo "Iniciando Hadoop MapReduce..."

hadoop jar \
    "$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar" \
    -D mapreduce.framework.name=local \
    -D fs.defaultFS=file:/// \
    -D mapreduce.job.reduces=1 \
    -files /opt/mapreduce/mapper.py,/opt/mapreduce/reducer.py \
    -input "$ENTRADA" \
    -output "$SALIDA" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"

test -f "$SALIDA/_SUCCESS"
test -s "$SALIDA/part-00000"

echo "MapReduce terminado correctamente."
