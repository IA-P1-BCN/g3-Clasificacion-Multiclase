"""Imagen del árbol para la diapositiva 18: los dos primeros niveles grandes
(el vigor resaltado) y el resto difuminado, con «…» donde sigue el árbol.

Uso, desde la raíz del repo: python docs/presentaciones/imagen_arbol.py
Genera docs/img/arbol_primeros_niveles.png a partir de models/03_arbol_decision.joblib.
"""
from pathlib import Path

import joblib
import matplotlib
from matplotlib.colors import to_rgb

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "docs" / "img" / "arbol_primeros_niveles.png"

modelo = joblib.load(RAIZ / "models" / "03_arbol_decision.joblib")
arbol = modelo["arbol"]
nombres = list(modelo["preprocesado"].get_feature_names_out())
fig, ax = plt.subplots(figsize=(16, 5.4), dpi=110)
notas = plot_tree(arbol, feature_names=nombres, class_names=list(arbol.classes_), max_depth=2,
                  filled=True, rounded=True, impurity=False, fontsize=22, proportion=True,
                  label="none", precision=2, ax=ax)


def num(texto):
    return texto.replace(".", ",")


def aclarar(caja, cuanto=0.75):
    r, g, b = to_rgb(caja.get_facecolor())
    caja.set_facecolor((r + (1 - r) * cuanto, g + (1 - g) * cuanto, b + (1 - b) * cuanto))
    caja.set_edgecolor("#cccccc")


for nota in notas:
    texto = nota.get_text()
    caja = nota.get_bbox_patch()
    flecha = getattr(nota, "arrow_patch", None)
    if "(...)" in texto:  # donde sigue el árbol
        nota.set_text("…")
        nota.set_color("#999999")
        aclarar(caja, 0.9)
        if flecha: flecha.set_alpha(0.25)
        continue
    if texto.strip() in ("True", "False"):
        nota.set_text("sí" if "True" in texto else "no")
        continue
    lineas = [l for l in texto.split("\n") if l and not l.startswith("[")]
    pct = f"{float(lineas[-2].rstrip('%')):.0f} %"
    vigor = texto.startswith("Vig")
    if len(lineas) == 3:   # nodo con pregunta
        pct += " de las parcelas" if vigor else ""
        nota.set_text(f"{num(lineas[0]).replace('<=', '≤')}\n{pct}")
    else:                  # hoja
        nota.set_text(f"{pct}\n→ {lineas[-1]}")
    if vigor:
        caja.set_edgecolor("#1F7A58")
        caja.set_linewidth(4)
        nota.set_fontweight("bold")
    else:
        nota.set_color("#8a8a8a")
        aclarar(caja)
        if flecha: flecha.set_alpha(0.35)
plt.tight_layout()
plt.savefig(SALIDA, facecolor="white", bbox_inches="tight", pad_inches=0.1)
print(f"Imagen guardada en {SALIDA.relative_to(RAIZ)}")
