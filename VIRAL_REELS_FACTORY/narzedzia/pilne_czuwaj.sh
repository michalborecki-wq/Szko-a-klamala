#!/bin/bash
# Czuwanie „PILNE”: przegląd co 15 min w godz. 6–23 (Europe/Warsaw); kończy się przy pierwszym alarmie
# (sesja główna wtedy weryfikuje temat i robi rolkę), potem uruchamia się ponownie.
cd "$(dirname "$0")"
while true; do
  h=$(TZ=Europe/Warsaw date +%H)
  if [ "$h" -ge 6 ] && [ "$h" -lt 23 ]; then
    out=$(python3 pilne.py --godziny 6 2>/dev/null)
    if [ -n "$out" ]; then echo "$out"; exit 0; fi
  fi
  sleep 900
done
