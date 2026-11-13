#!/usr/bin/env bash
# Graphify (graf wiedzy projektu) – instaluje CLI w osobnym środowisku, jeśli go nie ma, i uruchamia polecenie.
#   bash scripts/graphify.sh update .                 # odśwież graf po zmianach (bez LLM, 0 zł)
#   bash scripts/graphify.sh query "pytanie" --budget 1500
#   bash scripts/graphify.sh explain "render_all()"   |   affected "tpl()"   |   god-nodes
set -e
V=/opt/graphify-venv
if [ ! -x "$V/bin/graphify" ]; then
  python3 -m venv "$V" && "$V/bin/pip" install -q "graphifyy==0.9.108"
fi
exec "$V/bin/graphify" "$@"
