# Despliegue en Azure Kubernetes Service (AKS)

Unidad 3, Contenerización de Aplicaciones de Software. Dos aplicaciones distintas en un mismo clúster AKS:

| Aplicación | Tipo | Objetos de Kubernetes |
|---|---|---|
| Tienda (Node.js + MySQL) | Con estado | Namespace, ConfigMap, Secret, StatefulSet + PVC (disco de Azure), Deployment, Service LoadBalancer, probes |
| whoami | Sin estado | Deployment (3 réplicas), Service LoadBalancer, HorizontalPodAutoscaler |

## Requisitos
- Azure CLI (`brew install azure-cli`) y kubectl (`brew install kubectl`), con `az login` hecho.
- Esta carpeta `aks/` copiada en la raíz del repositorio (junto a `web/` y `db/`).

## Pasos
```bash
bash aks/scripts/01-crear-infraestructura.sh   # 10-15 min: ACR, imágenes y clúster
bash aks/scripts/02-demo-grabacion.sh 1        # bloques 1 a 5, uno por toma de video
bash aks/scripts/99-borrar-todo.sh             # al terminar: borra todo y deja de consumir crédito
```

## Si algo falla
- **Azure for Students (nov. 2026):** solo permite chilecentral, mexicocentral, northcentralus, spaincentral y canadacentral, y no permite B2s ni D2s_v3. Funcionó `Standard_B2as_v2` en `northcentralus`. ACR Tasks tampoco está permitido: las imágenes se construyen con Docker Desktop abierto.
- **La región no está permitida** (Azure for Students limita regiones): cambia `LOCATION` en `scripts/variables.sh`. Para ver las permitidas: `az policy assignment list --query "[].parameters.listOfAllowedLocations.value" -o tsv`.
- **El tamaño de máquina no está disponible**: cambia `NODE_SIZE` a `Standard_D2s_v3` o `Standard_B2s_v2`.
- **Cupo de vCPU excedido**: deja `NODE_COUNT=2` con máquinas de 2 vCPU (4 vCPU en total).
- **`az acr build` no permitido**: el script construye con Docker local (`docker buildx --platform linux/amd64`); Docker Desktop debe estar abierto.

## Costo aproximado
Plano de control gratis (nivel Free). Se pagan los 2 nodos B2as_v2, los discos, 2 IP públicas y el ACR Basic: menos de 1 USD por hora. Ejecuta `99-borrar-todo.sh` apenas termines de grabar.
