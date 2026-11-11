import csv
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

MATRICULA = 125053235

entrada = Path(f"data/ventas_{MATRICULA}.csv")
salida = Path("resultados/secuencial.tsv")

if not entrada.exists():
    raise SystemExit(f"ERROR: No existe {entrada}")

salida.parent.mkdir(parents=True, exist_ok=True)

totales = defaultdict(int)
registros = 0
errores = 0

inicio = time.perf_counter()

with entrada.open("r", encoding="utf-8", newline="") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        try:
            fecha = datetime.strptime(
                fila["fecha_hora"],
                "%Y-%m-%d %H:%M:%S"
            )

            metodo = fila["metodo_pago"].strip()
            cantidad = int(fila["cantidad"])

            if not metodo or cantidad < 0:
                errores += 1
                continue

            dia = fecha.weekday()
            clave = f"{metodo}|{dia}"

            totales[clave] += cantidad
            registros += 1

        except (ValueError, KeyError, TypeError, AttributeError):
            errores += 1

tiempo = time.perf_counter() - inicio

with salida.open("w", encoding="utf-8") as archivo:
    for clave in sorted(totales):
        archivo.write(f"{clave}\t{totales[clave]}\n")

print(f"Matricula: {MATRICULA}")
print(f"Registros procesados: {registros:,}")
print(f"Registros descartados: {errores:,}")
print(f"Combinaciones obtenidas: {len(totales)}")
print(f"Tiempo secuencial: {tiempo:.4f} segundos")
print(f"Resultados guardados en: {salida}")
