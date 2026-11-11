import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)


@contextmanager
def conexion_db():
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"]
    )
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "proyecto": "Examen Segundo Parcial - DataMart",
        "alumno": "Miguel Torres Martinez",
        "matricula": "125053235",
        "endpoints": [
            "GET /resultados",
            "GET /resultados/<clave>",
            "POST /resultados",
            "PUT /resultados/id/<id>",
            "DELETE /resultados/id/<id>"
        ]
    })


@app.route("/resultados", methods=["GET"])
def consultar_resultados():
    with conexion_db() as conexion:
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT id, metodo_pago, dia_semana, unidades_vendidas
                FROM resultados
                ORDER BY metodo_pago, dia_semana
            """)
            datos = cursor.fetchall()

    return jsonify({
        "total": len(datos),
        "resultados": datos
    })


@app.route("/resultados/<path:clave>", methods=["GET"])
def consultar_clave(clave):
    with conexion_db() as conexion:
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            if "|" in clave:
                metodo, dia = clave.rsplit("|", 1)
                try:
                    dia = int(dia)
                except ValueError:
                    return jsonify({"error": "Dia invalido"}), 400

                cursor.execute("""
                    SELECT id, metodo_pago, dia_semana, unidades_vendidas
                    FROM resultados
                    WHERE metodo_pago = %s AND dia_semana = %s
                """, (metodo, dia))
            else:
                cursor.execute("""
                    SELECT id, metodo_pago, dia_semana, unidades_vendidas
                    FROM resultados
                    WHERE metodo_pago = %s
                    ORDER BY dia_semana
                """, (clave,))

            datos = cursor.fetchall()

    if not datos:
        return jsonify({"error": "No se encontraron resultados"}), 404

    return jsonify({
        "total": len(datos),
        "resultados": datos
    })


def validar_datos(datos):
    if not isinstance(datos, dict):
        return None, "Se requiere un objeto JSON"

    try:
        metodo = datos["metodo_pago"]
        dia = datos["dia_semana"]
        unidades = datos["unidades_vendidas"]

        if not isinstance(metodo, str) or not metodo.strip():
            return None, "Metodo de pago invalido"

        if isinstance(dia, bool) or not isinstance(dia, int):
            return None, "Dia de semana invalido"

        if isinstance(unidades, bool) or not isinstance(unidades, int):
            return None, "Unidades vendidas invalidas"

        if dia < 0 or dia > 6 or unidades < 0:
            return None, "Valores fuera de rango"

        return (metodo.strip(), dia, unidades), None

    except KeyError:
        return None, "Faltan campos obligatorios"


@app.route("/resultados", methods=["POST"])
def agregar_resultado():
    valores, error = validar_datos(request.get_json(silent=True))

    if error:
        return jsonify({"error": error}), 400

    try:
        with conexion_db() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO resultados
                    (metodo_pago, dia_semana, unidades_vendidas)
                    VALUES (%s, %s, %s)
                    RETURNING id, metodo_pago, dia_semana, unidades_vendidas
                """, valores)
                nuevo = cursor.fetchone()

        return jsonify(nuevo), 201

    except psycopg2.IntegrityError:
        return jsonify({"error": "La combinacion ya existe"}), 409


@app.route("/resultados/id/<int:identificador>", methods=["PUT"])
def actualizar_resultado(identificador):
    valores, error = validar_datos(request.get_json(silent=True))

    if error:
        return jsonify({"error": error}), 400

    try:
        with conexion_db() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    UPDATE resultados
                    SET metodo_pago = %s,
                        dia_semana = %s,
                        unidades_vendidas = %s
                    WHERE id = %s
                    RETURNING id, metodo_pago, dia_semana, unidades_vendidas
                """, (*valores, identificador))
                actualizado = cursor.fetchone()

        if actualizado is None:
            return jsonify({"error": "Registro no encontrado"}), 404

        return jsonify(actualizado)

    except psycopg2.IntegrityError:
        return jsonify({"error": "La combinacion ya existe"}), 409


@app.route("/resultados/id/<int:identificador>", methods=["DELETE"])
def eliminar_resultado(identificador):
    with conexion_db() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM resultados WHERE id = %s RETURNING id",
                (identificador,)
            )
            eliminado = cursor.fetchone()

    if eliminado is None:
        return jsonify({"error": "Registro no encontrado"}), 404

    return jsonify({
        "mensaje": "Registro eliminado correctamente",
        "id": identificador
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
