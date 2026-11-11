import sys
import csv
from datetime import datetime

reader = csv.reader(sys.stdin)

for row in reader:
    if not row or row[0] == "venta_id":
        continue

    if len(row) != 8:
        continue

    try:
        fecha = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        cantidad = int(row[4])
        metodo_pago = row[6].strip()

        if cantidad < 0 or not metodo_pago:
            continue

        dia_semana = fecha.weekday()

        print(f"{metodo_pago}|{dia_semana}\t{cantidad}")

    except (ValueError, IndexError):
        continue
