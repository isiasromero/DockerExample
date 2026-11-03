# Variables comunes. Ajusta LOCATION si Azure for Students no permite la region.
export RG="rg-tienda-aks"
export LOCATION="canadacentral"       # grupo de recursos y ACR
export AKS_LOCATION="northcentralus"  # cluster: region que permite B2as_v2 en Azure for Students
export AKS="aks-tienda"
export NODE_SIZE="Standard_B2as_v2"  # 2 vCPU AMD x86, 8 GB. Azure for Students no permite B2s ni D2s_v3
export NODE_COUNT=2
# Nombre del registro: unico en Azure, solo letras minusculas y numeros
SUB_ID=$(az account show --query id -o tsv 2>/dev/null)
export ACR="acrtienda${SUB_ID:0:6}"
export ACR_LOGIN="${ACR}.azurecr.io"
