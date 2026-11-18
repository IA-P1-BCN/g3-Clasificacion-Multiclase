"""Publica solo la presentación en GitHub Pages (rama gh-pages), no el resto del repo.

La rama gh-pages solo contiene la presentación, como index.html, y un .nojekyll.
Pages la sirve en https://ia-p1-bcn.github.io/g3-Clasificacion-Multiclase/

Uso, desde la raíz del repo y con la presentación ya mergeada en main:
    python docs/presentaciones/publicar_pages.py

No toca la rama ni los ficheros de trabajo: crea el commit con git plumbing y lo
sube a origin/gh-pages, encima del anterior para conservar el historial.
"""

import subprocess
import sys
from pathlib import Path

PRESENTACION = Path(__file__).resolve().parent / "presentacion-eucalyptus.html"
RAMA = "gh-pages"


def git(*argumentos, entrada=None):
    resultado = subprocess.run(
        ["git", *argumentos], input=entrada, capture_output=True, text=True, check=True
    )
    return resultado.stdout.strip()


def main():
    # Último commit publicado (si ya existe la rama), para encadenar el historial
    anterior = git("ls-remote", "--heads", "origin", RAMA).split("\t")[0] or None
    if anterior:
        git("fetch", "--quiet", "origin", RAMA)

    pagina = git("hash-object", "-w", str(PRESENTACION))
    vacio = git("hash-object", "-w", "--stdin", entrada="")
    arbol = git(
        "mktree",
        entrada=f"100644 blob {vacio}\t.nojekyll\n100644 blob {pagina}\tindex.html\n",
    )
    if anterior and git("rev-parse", f"{anterior}^{{tree}}") == arbol:
        print("La presentación publicada ya es esta versión: no hay nada que subir.")
        return 0

    origen = git("rev-parse", "--short", "HEAD")
    padres = ["-p", anterior] if anterior else []
    mensaje = f"docs: publicar la presentación ({origen})"
    commit = git("commit-tree", arbol, *padres, "-m", mensaje)
    git("push", "origin", f"{commit}:refs/heads/{RAMA}")
    print(f"Publicada en {RAMA} ({commit[:7]}). Pages tarda un minuto en actualizarse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
