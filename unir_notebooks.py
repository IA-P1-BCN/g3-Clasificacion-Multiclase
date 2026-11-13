"""Junta los notebooks del proyecto, en orden, en final.ipynb (con nbmerge).

Uso: python unir_notebooks.py
Los notebooks que aún no existen se saltan con un aviso.
"""

import io
import uuid
from pathlib import Path

from nbformat import write
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


def main():
    existentes = [RAIZ / nombre for nombre in ORDEN if (RAIZ / nombre).exists()]
    for nombre in ORDEN:
        if not (RAIZ / nombre).exists():
            print(f"⚠️ Falta {nombre}: no se incluye")
    if not existentes:
        raise SystemExit("No hay ningún notebook que unir.")
    final = merge_notebooks(str(RAIZ), [str(ruta) for ruta in existentes])
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
