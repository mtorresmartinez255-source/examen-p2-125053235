import os
import sys
from pathlib import Path

import psycopg2

ARCHIVO = Path("/app/resultados/resultado/part-00000")

if not ARCHIVO.exists():
    sys.exit(f"ERROR: No existe {ARCHIVO}")

conexion = psycopg2.connect(
    host=os.environ.get("DB_HOST", "db"),
    port=int(os.environ.get("DB_PORT", "5432")),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"]
)

with conexion:
    with conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id SERIAL PRIMARY KEY,
                metodo_pago VARCHAR(50) NOT NULL,
                dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 0 AND 6),
                unidades_vendidas BIGINT NOT NULL CHECK (unidades_vendidas >= 0),
                UNIQUE (metodo_pago, dia_semana)
            )
        """)

        registros = 0

        with ARCHIVO.open("r", encoding="utf-8") as archivo:
            for linea in archivo:
                clave, unidades = linea.rstrip("\n").split("\t", 1)
                metodo_pago, dia = clave.rsplit("|", 1)

                cursor.execute("""
                    INSERT INTO resultados
                    (metodo_pago, dia_semana, unidades_vendidas)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (metodo_pago, dia_semana)
                    DO UPDATE SET
                    unidades_vendidas = EXCLUDED.unidades_vendidas
                """, (metodo_pago, int(dia), int(unidades)))

                registros += 1

conexion.close()

print("Carga completada correctamente")
print(f"Registros cargados: {registros}")
