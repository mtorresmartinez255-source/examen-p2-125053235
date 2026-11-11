FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY generar_dataset.py .
COPY generador/iniciar.sh .

RUN chmod +x iniciar.sh

CMD ["./iniciar.sh"]
