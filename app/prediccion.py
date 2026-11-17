"""Lógica de la app, separada de la interfaz (no importa streamlit).

Carga el modelo ganador, valida los datos de una parcela y predice su clase de
utilidad. Las parcelas sin medidas se responden `none` por regla fija, sin pasar
por el modelo (ADR-0001), con `predecir_con_regla` de `comun.py`.
"""

from dataclasses import dataclass

import joblib
import numpy as np
import pandas as pd

from comun import MODELOS, cargar_resultados, predecir_con_regla, sin_medidas

# Etiquetas en español de cada variable del formulario
ETIQUETAS = {
    "Abbrev": "Sitio del ensayo",
    "DBH": "Diámetro del tronco (cm)",
    "Ht": "Altura (m)",
    "Surv": "Supervivencia (%)",
    "Vig": "Vigor (0-5)",
    "Ins_res": "Resistencia a insectos (0-5)",
    "Stem_Fm": "Forma del tronco (0-5)",
    "Crown_Fm": "Forma de la copa (0-5)",
    "Brnch_Fm": "Forma de las ramas (0-5)",
}
# Rangos posibles: (mínimo, máximo, si el mínimo vale). En los datos, DBH llega a
# 54 cm y Ht a 22 m: los máximos son generosos y solo paran erratas (DBH = 42 085).
RANGOS = {
    "DBH": (0, 200, False),
    "Ht": (0, 60, False),
    "Surv": (0, 100, True),
    "Vig": (0, 5, True),
    "Ins_res": (0, 5, True),
    "Stem_Fm": (0, 5, True),
    "Crown_Fm": (0, 5, True),
    "Brnch_Fm": (0, 5, True),
}
# Los 16 sitios del ensayo. Mor y Wen solo tienen parcelas sin medidas, así que el
# modelo no los vio al entrenar (ver `sitios_del_modelo`).
SITIOS = sorted(
    "Cly Cra K81 K81a K82 K83 Lon Mor Nga Paw Puk WSh WSp Wai Wak Wen".split()
)
SITIO_DESCONOCIDO = "Otro / desconocido"


class EntradaInvalida(ValueError):
    """Datos imposibles: no se predice. `errores` trae un mensaje por campo."""

    def __init__(self, errores):
        self.errores = errores
        super().__init__("; ".join(errores))


@dataclass(frozen=True)
class Prediccion:
    """Resultado de predecir una parcela."""

    clase: str
    por_regla: bool  # True si es `none` por ser una parcela sin medidas
    faltan: list  # variables vacías: el pipeline las completa con la mediana
    sitio_conocido: bool  # False si el modelo no vio ese sitio al entrenar


def nombre_ganador():
    """El modelo ganador: el primero que cumple el gap en cargar_resultados() (06)."""
    resultados = cargar_resultados()
    cumplen = resultados[resultados["cumple_gap"]]
    if cumplen.empty:
        raise RuntimeError("Ningún modelo cumple el gap: no hay modelo ganador.")
    return cumplen.index[0]


def cargar_modelo(nombre=None):
    """Carga el pipeline de models/<nombre>.joblib (por defecto, el ganador)."""
    return joblib.load(MODELOS / f"{nombre or nombre_ganador()}.joblib")


def predecir(modelo, datos):
    """Predice la clase de una parcela. `datos`: {variable: valor} del formulario."""
    variables = list(modelo.feature_names_in_)
    fila = validar(modelo, datos)
    X = pd.DataFrame([fila], columns=variables)
    clase = predecir_con_regla(modelo, X).iloc[0]
    return Prediccion(
        clase=clase,
        por_regla=bool(sin_medidas(X).iloc[0]),
        faltan=[v for v in variables if v != "Abbrev" and pd.isna(fila[v])],
        sitio_conocido=fila.get("Abbrev") in sitios_del_modelo(modelo),
    )


def sitios_del_modelo(modelo):
    """Los sitios que el modelo vio al entrenar (categorías del one-hot de `Abbrev`)."""
    for _, transformador, columnas in modelo[0].transformers_:
        if "Abbrev" in list(columnas):
            # El codificador es el último paso si el transformador es un Pipeline
            pasos = getattr(transformador, "steps", [(None, transformador)])
            codificador = pasos[-1][1]
            return list(codificador.categories_[list(columnas).index("Abbrev")])
    return []


def validar(modelo, datos):
    """Comprueba los datos y los devuelve listos para el modelo (vacío → NaN).

    Lanza EntradaInvalida con todos los errores a la vez si hay algún valor
    imposible: texto en un número, fuera de rango o un sitio que no existe.
    """
    fila, errores = {}, []
    for variable in modelo.feature_names_in_:
        valor = datos.get(variable)
        etiqueta = ETIQUETAS.get(variable, variable)
        if variable == "Abbrev":
            if _vacio(valor) or valor == SITIO_DESCONOCIDO:
                fila[variable] = SITIO_DESCONOCIDO
            elif valor in SITIOS:
                fila[variable] = valor
            else:
                errores.append(f"{etiqueta}: «{valor}» no es un sitio del ensayo.")
            continue
        if _vacio(valor):
            fila[variable] = np.nan
            continue
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            errores.append(f"{etiqueta}: «{valor}» no es un número.")
            continue
        minimo, maximo, minimo_incluido = RANGOS.get(variable, (-np.inf, np.inf, True))
        por_debajo = numero < minimo if minimo_incluido else numero <= minimo
        if por_debajo or numero > maximo:
            desde = "desde" if minimo_incluido else "mayor que"
            errores.append(
                f"{etiqueta}: {numero:g} es imposible (tiene que ser {desde} "
                f"{minimo:g} y como mucho {maximo:g})."
            )
        fila[variable] = numero
    if errores:
        raise EntradaInvalida(errores)
    return fila


def _vacio(valor):
    """Un campo sin rellenar: None, texto vacío o NaN."""
    if valor is None:
        return True
    if isinstance(valor, str):
        return valor.strip() == ""
    return isinstance(valor, float) and np.isnan(valor)
