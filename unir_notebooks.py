"""Junta los notebooks del proyecto, en orden, en final.ipynb (con nbmerge).

Uso: python unir_notebooks.py
Los notebooks que aún no existen se saltan con un aviso. Al principio se añade una
celda que, solo en Google Colab, descarga el repo (comun.py y data/) y sus requisitos.
"""

import io
import uuid
from pathlib import Path

from nbformat import write
from nbformat.v4 import new_code_cell
from nbmerge import merge_notebooks

RAIZ = Path(__file__).resolve().parent
ORDEN = [
    "00_general.ipynb",
    "01_eda.ipynb",
    "02_regresion_logistica.ipynb",
    "03_arbol_decision.ipynb",
    "04_svm.ipynb",
    "05_knn.ipynb",
    "06_conclusiones.ipynb",
]
SALIDA = RAIZ / "final.ipynb"
REPO = "https://github.com/IA-P1-BCN/g3-Clasificacion-Multiclase"
CELDA_COLAB = f"""# Preparación para Google Colab (en local no hace nada)
import os
import subprocess
import sys

if "google.colab" in sys.modules and not os.path.exists("comun.py"):
    carpeta = "/content/g3-Clasificacion-Multiclase"
    if not os.path.exists(carpeta):
        subprocess.run(["git", "clone", "--depth", "1", "{REPO}", carpeta], check=True)
    os.chdir(carpeta)
    sys.path.insert(0, carpeta)
    instalado = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"]
    )
    if instalado.returncode != 0:
        print("⚠️ No se han podido instalar todas las versiones fijadas; "
              "se usan las de Colab.")"""


def main():
    existentes = [RAIZ / nombre for nombre in ORDEN if (RAIZ / nombre).exists()]
    for nombre in ORDEN:
        if not (RAIZ / nombre).exists():
            print(f"⚠️ Falta {nombre}: no se incluye")
    if not existentes:
        raise SystemExit("No hay ningún notebook que unir.")
    final = merge_notebooks(str(RAIZ), [str(ruta) for ruta in existentes])
    final.cells.insert(0, new_code_cell(CELDA_COLAB))
    # Varios notebooks comparten ids de celda (01 nació como copia de 00): se renuevan
    vistos = set()
    for celda in final.cells:
        if celda.get("id") in vistos or "id" not in celda:
            celda["id"] = uuid.uuid4().hex[:8]
        vistos.add(celda["id"])
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fichero:
        write(final, fichero)
    print(f"{SALIDA.name}: {len(existentes)} notebooks, {len(final.cells)} celdas")


if __name__ == "__main__":
    main()
