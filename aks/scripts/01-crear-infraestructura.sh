#!/usr/bin/env bash
# Crea grupo de recursos, registro de imagenes (ACR), construye las imagenes en Azure y crea el cluster AKS.
# Ejecutar desde la raiz del repositorio (donde estan las carpetas web/ y db/).
set -euo pipefail
cd "$(dirname "$0")/../.."; [ -f web/Dockerfile ] || { echo "Ejecuta desde el repo con web/ y db/"; exit 1; }
source aks/scripts/variables.sh

echo "== Registrando proveedores (solo la primera vez, tarda 1-2 min)"
for p in Microsoft.ContainerService Microsoft.ContainerRegistry Microsoft.Compute Microsoft.Network Microsoft.Storage Microsoft.OperationalInsights; do
  az provider register --namespace $p --wait
done

echo "== Grupo de recursos $RG en $LOCATION"
az group create -n "$RG" -l "$LOCATION" -o table

echo "== Registro de imagenes $ACR"
az acr create -g "$RG" -n "$ACR" --sku Basic -o table

echo "== Construyendo las imagenes (amd64, la arquitectura de los nodos de AKS)"
if ! az acr build -r "$ACR" -t tienda-web:1.0 ./web; then
  echo "ACR Tasks no disponible en esta suscripcion; se construye con Docker local"
  az acr login -n "$ACR"
  docker buildx build --platform linux/amd64 -t "$ACR_LOGIN/tienda-web:1.0" --push ./web
  docker buildx build --platform linux/amd64 -t "$ACR_LOGIN/tienda-mysql:1.0" --push ./db
else
  az acr build -r "$ACR" -t tienda-mysql:1.0 ./db
fi

echo "== Cluster AKS (nivel Free, $NODE_COUNT nodos $NODE_SIZE). Tarda 5-8 min"
az aks create -g "$RG" -n "$AKS" -l "$AKS_LOCATION" \
  --tier free --node-count "$NODE_COUNT" --node-vm-size "$NODE_SIZE" \
  --attach-acr "$ACR" --generate-ssh-keys -o table

az aks get-credentials -g "$RG" -n "$AKS" --overwrite-existing
kubectl get nodes -o wide
echo "Listo. Siguiente: aks/scripts/02-demo-grabacion.sh"
