#!/bin/sh
# Repite la verificación: 1.000 conjuntos de datos simulados por procedimiento.
# Requiere Node.js y Python con NumPy y SciPy.
set -e
cd "$(dirname "$0")"
python3 extraer_funciones.py ../web/Kenti-Libre-0.3.html   # extrae las funciones de cálculo, sin modificarlas
python3 generar_datos.py                                    # simula los datos (semilla 20260921)
node ejecutar_kenti.js                                      # calcula con las funciones de Kenti
python3 comparar.py                                         # compara con NumPy y SciPy
