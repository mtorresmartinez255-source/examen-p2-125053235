import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

MATRICULA = 125053235
TOTAL = 5_000_000

random.seed(MATRICULA)

Path("data").mkdir(exist_ok=True)
archivo = Path(f"data/ventas_{MATRICULA}.csv")

if archivo.exists():
    print(f"El dataset ya existe: {archivo}")
    raise SystemExit(0)

categorias = [
    "Alimentos",
    "Electronica",
    "Ropa",
    "Hogar",
    "Deportes"
]

metodos_pago = [
    "Efectivo",
    "Tarjeta",
    "Transferencia",
    "Vales"
]

fecha_inicio = datetime(2025, 1, 1)

with archivo.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "venta_id",
        "fecha_hora",
        "producto_id",
        "categoria",
        "cantidad",
        "precio_unitario",
        "metodo_pago",
        "sucursal"
    ])

    for i in range(1, TOTAL + 1):
        fecha = fecha_inicio + timedelta(
            minutes=random.randint(0, 525599)
        )

        writer.writerow([
            i,
            fecha.strftime("%Y-%m-%d %H:%M:%S"),
            random.randint(1, 1000),
            random.choice(categorias),
            random.randint(1, 10),
            round(random.uniform(10, 5000), 2),
            random.choice(metodos_pago),
            f"S{random.randint(1, 20):03d}"
        ])

print(f"Dataset generado correctamente: {archivo}")
print(f"Total de registros: {TOTAL}")
