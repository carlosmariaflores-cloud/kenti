#!/bin/sh
# Regenera las Figuras 1 y 2 del manuscrito. Requiere Node.js, Python (NumPy, Matplotlib, Pillow) y Playwright con Chromium.
set -e
cd "$(dirname "$0")"
python3 ../verificacion/extraer_funciones.py ../web/Kenti-Libre-0.3.html
mv kenti_core.js ../verificacion/kenti_core.js 2>/dev/null || true
python3 simular_aves.py
python3 capturar_panel_a_c.py && python3 capturar_panel_d.py && python3 componer_figura1.py    # figura1.png
python3 fig2_simular.py && node fig2_calcular.js && python3 fig2_graficar.py                    # figura2.png
