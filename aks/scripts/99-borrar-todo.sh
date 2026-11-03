#!/usr/bin/env bash
# Borra TODO lo creado (cluster, discos, IPs, registro) para no consumir credito.
source "$(dirname "$0")/variables.sh"
az group delete -n "$RG" --yes --no-wait
echo "Borrando $RG en segundo plano. Verifica en unos minutos con: az group list -o table"
