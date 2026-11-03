# Efecto de escritura para grabar: comentario verde, comando amarillo, pausa.
TECLA=${TECLA:-0.07}; PAUSA=${PAUSA:-6}
_teclear(){ local s="$1" i; for ((i=0;i<${#s};i++)); do printf '%s' "${s:$i:1}"; sleep $TECLA; done; }
titulo(){ printf '\n\033[1;32m'; _teclear "# ===== $1 ====="; printf '\033[0m\n'; sleep 2; }
paso(){ # paso "explicacion" "comando" [pausa]
  printf '\033[32m$ '; _teclear "# $1"; printf '\033[0m\n'; sleep 2
  printf '\033[0;37m$ \033[1;33m'; _teclear "$2"; printf '\033[0m\n'; sleep 1
  eval "$2"; echo; sleep "${3:-$PAUSA}"
}
esperar_ip(){ # esperar_ip namespace servicio
  printf '\033[2mEsperando la IP publica del balanceador de Azure...\033[0m\n'
  until IP=$(kubectl get svc -n "$1" "$2" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null) && [ -n "$IP" ]; do sleep 5; done
  echo "IP publica: $IP"; export IP
}
