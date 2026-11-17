"""Junta los notebooks del proyecto, en orden, en final.ipynb (con nbmerge).

Uso: python unir_notebooks.py
Los notebooks que aún no existen se saltan con un aviso. Al principio se añaden:
- un índice con enlaces a cada notebook y a sus secciones (`#scrollTo=` de Colab);
- una celda que, solo en Google Colab, descarga el repo (comun.py y data/) y sus
  requisitos.
"""

import io
import re
import uuid
from pathlib import Path

from nbformat import read, write
from nbformat.v4 import new_code_cell, new_markdown_cell
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
              "se usan las de Colab.")
    # Si Colab ya tenía cargada otra versión de una librería, hay que reiniciar
    from importlib.metadata import version
    librerias = {{"numpy": "numpy", "pandas": "pandas", "sklearn": "scikit-learn",
                  "scipy": "scipy", "matplotlib": "matplotlib"}}
    if any(modulo in sys.modules and sys.modules[modulo].__version__ != version(paquete)
           for modulo, paquete in librerias.items()):
        print("🔄 Versiones nuevas instaladas: se reinicia la sesión. "
              "Vuelve a ejecutar todo (Entorno de ejecución > Ejecutar todas).")
        os.kill(os.getpid(), 9)"""
# Atajos del índice: (texto, notebook, regex con el que empieza el título)
ATAJOS = [
    ("Conclusión del EDA", "01_eda", r"📝 Conclusión del EDA"),
    ("Tabla comparativa de los modelos", "06_conclusiones", r"Paso 3:"),
    ("Elección del modelo ganador", "06_conclusiones", r"Paso 5:"),
    ("Evaluación final en test", "06_conclusiones", r"Paso 6:"),
    ("Requisitos del Nivel Esencial", "06_conclusiones", r"Paso 10:"),
    ("Conclusiones para negocio", "06_conclusiones", r"Conclusiones$"),
]
INTRO = """# g3 · Clasificación multiclase (Eucalyptus): notebook final

Predecimos la **clase de utilidad** de una parcela de eucalipto para conservar el \
suelo (`none` < `low` < `average` < `good` < `best`). Este notebook junta, en \
orden, todos los notebooks del proyecto: problema y split, EDA, los cuatro \
modelos y las conclusiones. Repo: [{repo}]({repo}).

**Cómo usarlo**
- Ya está ejecutado: se puede leer sin ejecutar nada.
- Para ejecutarlo en Colab: *Entorno de ejecución > Ejecutar todas*. La primera \
celda de código descarga el repo e instala los requisitos.
- Los enlaces del índice saltan a cada sección en Colab. En Jupyter o VS Code, \
usa el panel de esquema (*Outline*) o el índice lateral.
"""


def titulos(celda):
    """Títulos de nivel 1 y 2 de una celda markdown (sin los #)."""
    if celda.cell_type != "markdown":
        return []
    return [
        re.sub(r"^#{1,2} ", "", linea).strip()
        for linea in celda.source.splitlines()
        if re.match(r"^#{1,2} ", linea)
    ]


def enlace(texto, ancla):
    texto = texto.replace("[", "(").replace("]", ")")
    return f"[{texto}](#scrollTo={ancla})"


def anadir_indice(final, rutas):
    """Pone anclas en las celdas con títulos y devuelve la celda del índice.

    Colab usa el id de `metadata` para `#scrollTo=`; se copia también en el id
    de la celda para que el ancla no cambie al regenerar.
    """
    inicio, lineas, anclas, parte = 0, [], {}, 0
    for ruta in rutas:
        prefijo = ruta.stem[:2]
        celdas = final.cells[inicio : inicio + len(read(ruta, as_version=4).cells)]
        inicio += len(celdas)
        apartados = []
        for n, celda in enumerate(c for c in celdas if titulos(c)):
            ancla = f"nb{prefijo}" if n == 0 else f"nb{prefijo}-{n}"
            celda["id"] = celda.metadata["id"] = ancla
            for titulo in titulos(celda):
                anclas[(ruta.stem, titulo)] = ancla
                apartados.append((titulo, ancla))
        if not apartados:
            continue
        parte += 1
        principal, ancla = apartados[0]
        lineas.append(f"{parte}. **{enlace(principal, ancla)}** · `{ruta.name}`")
        lineas += [f"    - {enlace(t, a)}" for t, a in apartados[1:]]
    atajos = [
        f"- {enlace(texto, ancla)}"
        for texto, notebook, patron in ATAJOS
        for (nb, titulo), ancla in anclas.items()
        if nb == notebook and re.match(patron, titulo)
    ]
    texto = INTRO.format(repo=REPO)
    if atajos:
        texto += "\n**Atajos**\n" + "\n".join(dict.fromkeys(atajos)) + "\n"
    texto += "\n## Índice\n" + "\n".join(lineas)
    return new_markdown_cell(texto)


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
    indice = anadir_indice(final, existentes)
    final.cells[:0] = [indice, new_code_cell(CELDA_COLAB)]
    for celda in final.cells[:2]:
        celda["id"] = celda.metadata["id"] = "indice" if celda is indice else "colab"
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fichero:
        write(final, fichero)
    print(f"{SALIDA.name}: {len(existentes)} notebooks, {len(final.cells)} celdas")


if __name__ == "__main__":
    main()
