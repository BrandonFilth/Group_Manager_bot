#!/bin/bash

#Ruta del script
SCRIPT_PATH="/main.py"

INTERVAL=2

while true; do
    #Comprobar si el script esta en ejecucion
    if ! pgrep -f $SCRIPT_PATH > /dev/null; then
        echo "El Script se detuvo"
        python3 $SCRIPT_PATH &
    else
        echo "El script esta en ejecucion"

    fi
    #Tiempo de espera
    sleep $INTERVAL
done
