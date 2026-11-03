#!/usr/bin/env bash
# Lo abre grabar.py dentro de mintty: pausa inicial, bloque de la demo y pausa final.
cd "$(dirname "$0")/../.."; clear; sleep 4
bash aks/scripts/02-demo-grabacion.sh "$1"; sleep 6
