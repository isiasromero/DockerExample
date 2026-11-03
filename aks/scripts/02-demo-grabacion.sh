#!/usr/bin/env bash
# Demo para grabar: escribe cada comando con su explicacion y lo ejecuta.
# Uso: aks/scripts/02-demo-grabacion.sh [bloque]   (bloques: 1 2 3 4 5; sin argumento corre todos)
cd "$(dirname "$0")/../.."
source aks/scripts/variables.sh; source aks/scripts/lib.sh
B=${1:-todos}; clear
aplicar(){ sed "s|__ACR__|$ACR_LOGIN|g" "$1" | kubectl apply -f -; }

if [[ $B == todos || $B == 1 ]]; then
titulo "Bloque 1: el cluster AKS"
paso "Cluster administrado por Azure: nivel Free, plano de control sin costo" "az aks show -g $RG -n $AKS --query '{nombre:name, version:kubernetesVersion, nivel:sku.tier, region:location}' -o table"
paso "Nodos de trabajo: maquinas virtuales de Azure que ejecutan los pods" "kubectl get nodes -o wide"
paso "Componentes del sistema que Azure instala y mantiene" "kubectl get pods -n kube-system"
paso "Clases de almacenamiento: discos administrados de Azure para datos persistentes" "kubectl get storageclass"
paso "Imagenes propias en Azure Container Registry, conectado al cluster" "az acr repository list -n $ACR -o table"
fi

if [[ $B == todos || $B == 2 ]]; then
titulo "Bloque 2: aplicacion 1, tienda Node.js + MySQL (con estado)"
paso "Namespaces para separar las dos aplicaciones" "kubectl apply -f aks/k8s/01-namespaces.yaml"
paso "Configuracion en ConfigMap y claves en Secret" "kubectl apply -f aks/k8s/02-tienda-config.yaml"
paso "MySQL como StatefulSet con un disco persistente de Azure" "aplicar aks/k8s/03-mysql.yaml"
paso "Servidor web con 2 replicas y servicio LoadBalancer" "aplicar aks/k8s/04-tienda-web.yaml"
paso "Esperamos a que la base de datos este lista" "kubectl rollout status statefulset/mysql -n tienda --timeout=300s"
paso "Y el servidor web" "kubectl rollout status deployment/tienda-web -n tienda --timeout=300s"
paso "Pods, servicios y el volumen persistente creados" "kubectl get pods,svc,pvc -n tienda -o wide" 10
esperar_ip tienda tienda-web; echo "Abrir en el navegador: http://$IP"; export TIENDA_IP=$IP
paso "Cargamos los 15 productos en la base de datos" "kubectl exec -i -n tienda mysql-0 -- mysql -uapp -papp123 tienda < db/seed-productos.sql"
paso "La aplicacion responde desde Azure con los 15 productos" "curl -s http://$TIENDA_IP/api/productos | head -c 400; echo" 10
fi

if [[ $B == todos || $B == 3 ]]; then
titulo "Bloque 3: aplicacion 2, servicio web sin estado (whoami)"
paso "Deployment de 3 replicas, LoadBalancer y autoescalado (HPA)" "kubectl apply -f aks/k8s/05-whoami.yaml"
paso "Esperamos las replicas" "kubectl rollout status deployment/whoami -n whoami --timeout=180s"
esperar_ip whoami whoami; export WHO_IP=$IP
paso "Cada peticion la atiende un pod distinto: balanceo de carga" "for i in 1 2 3 4 5 6; do curl -s http://$WHO_IP | grep Hostname; done" 10
paso "Repartidos entre los dos nodos" "kubectl get pods -n whoami -o wide"
fi

if [[ $B == todos || $B == 4 ]]; then
titulo "Bloque 4: operacion, escalado, autorreparacion y actualizacion"
WHO_IP=$(kubectl get svc -n whoami whoami -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
paso "Escalado manual a 5 replicas" "kubectl scale deployment/whoami -n whoami --replicas=5 && kubectl rollout status deployment/whoami -n whoami"
paso "Autorreparacion: borramos un pod a proposito" "kubectl delete pod -n whoami \$(kubectl get pods -n whoami -o name | head -1 | cut -d/ -f2)"
paso "Kubernetes crea otro automaticamente para mantener el estado deseado" "kubectl get pods -n whoami" 8
paso "Actualizacion sin caida (rolling update) a una nueva version de la imagen" "kubectl set image deployment/whoami -n whoami whoami=traefik/whoami:v1.11.0 && kubectl rollout status deployment/whoami -n whoami"
paso "Historial de versiones" "kubectl rollout history deployment/whoami -n whoami"
paso "Volver a la version anterior (rollback)" "kubectl rollout undo deployment/whoami -n whoami && kubectl rollout status deployment/whoami -n whoami"
paso "El autoescalador (HPA) vigila el uso de CPU" "kubectl get hpa -n whoami"
fi

if [[ $B == todos || $B == 5 ]]; then
titulo "Bloque 5: persistencia de los datos en el disco de Azure"
TIENDA_IP=$(kubectl get svc -n tienda tienda-web -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
paso "Productos antes de borrar la base de datos" "kubectl exec -n tienda mysql-0 -- mysql -uapp -papp123 tienda -e 'SELECT COUNT(*) AS productos FROM productos;' 2>/dev/null"
paso "Borramos el pod de MySQL" "kubectl delete pod mysql-0 -n tienda"
paso "El StatefulSet lo recrea y vuelve a conectar el mismo disco" "kubectl rollout status statefulset/mysql -n tienda --timeout=300s"
paso "Los 15 productos siguen ahi" "kubectl exec -n tienda mysql-0 -- mysql -uapp -papp123 tienda -e 'SELECT COUNT(*) AS productos FROM productos;' 2>/dev/null" 10
paso "El disco persistente es un recurso de Azure independiente del pod" "kubectl get pvc -n tienda"
fi
printf '\n\033[1;32m# Fin de la demostracion\033[0m\n'
