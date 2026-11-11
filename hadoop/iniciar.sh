#!/bin/bash
set -euo pipefail

rm -f /tmp/hadoop-pipeline-ready

mkdir -p /run/sshd /ssh /home/hadoop/.ssh

chmod 700 /ssh

if [ ! -f /ssh/id_ed25519 ]; then
    ssh-keygen -t ed25519 \
      -f /ssh/id_ed25519 \
      -N "" \
      -C "hadoop-miguel-125053235"
fi

chmod 600 /ssh/id_ed25519
chmod 644 /ssh/id_ed25519.pub

cat /ssh/id_ed25519.pub > /home/hadoop/.ssh/authorized_keys

if [ -f /ssh-api-public/id_ed25519.pub ]; then
    cat /ssh-api-public/id_ed25519.pub >> /home/hadoop/.ssh/authorized_keys
fi

chown -R hadoop:hadoop /home/hadoop/.ssh
chmod 700 /home/hadoop/.ssh
chmod 600 /home/hadoop/.ssh/authorized_keys

/usr/sbin/sshd

echo "SSH iniciado correctamente."

if [ -f /data/output/resultado/_SUCCESS ] && [ -s /data/output/resultado/part-00000 ]; then
    echo "Resultados anteriores encontrados. No se repite MapReduce."
else
    /usr/local/bin/procesar.sh
fi

touch /tmp/hadoop-pipeline-ready

echo "Hadoop listo. Resultados disponibles."

