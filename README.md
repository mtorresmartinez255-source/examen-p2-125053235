# Examen segundo parcial - DataMart

Matrícula: 125053235

## Descripción

Proyecto de procesamiento de datos de ventas utilizando Docker, Hadoop MapReduce, PostgreSQL y una API desarrollada con Python y Flask.

Se generan 5,000,000 de registros de ventas y se procesan utilizando Hadoop Streaming.

El procesamiento agrupa las unidades vendidas por método de pago y día de la semana.

## Tecnologías utilizadas

- Docker y Docker Compose
- Hadoop 3.3.6
- Python 3
- PostgreSQL 16
- Flask

## Funcionamiento

1. El generador crea el archivo de ventas.
2. Hadoop procesa los registros mediante Mapper y Reducer.
3. Los resultados se almacenan en PostgreSQL.
4. Flask permite consultar y administrar los resultados.

## Ejecución

Configurar las variables de PostgreSQL:

cp .env.example .env

Editar el archivo .env y establecer una contraseña segura.

Después ejecutar:

docker compose up --build

## API

Puerto: 5056

GET /resultados

GET /resultados/Efectivo%7C0

POST /resultados

PUT /resultados/id/ID

DELETE /resultados/id/ID

## Resultados

Registros procesados: 5,000,000

Combinaciones obtenidas: 28

Métodos de pago: Efectivo, Tarjeta, Transferencia y Vales.

## Evidencias

La carpeta evidencias contiene los registros de ejecución de Docker, Hadoop, PostgreSQL y la API.
