#!/bin/sh
set -e

mkdir -p /app/data /app/ssh-api

if [ ! -f /app/ssh-api/id_ed25519 ]; then
    ssh-keygen -q -t ed25519 \
      -f /app/ssh-api/id_ed25519 \
      -N "" \
      -C "api-miguel-125053235"
fi

chmod 600 /app/ssh-api/id_ed25519
chmod 644 /app/ssh-api/id_ed25519.pub

python generar_dataset.py

echo "Dataset y llaves SSH preparados correctamente."
