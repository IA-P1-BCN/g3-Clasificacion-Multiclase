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


@dataclass(frozen=True)
class Prediccion:
    """Resultado de predecir una parcela."""

    clase: str
    por_regla: bool  # True si es `none` por ser una parcela sin medidas


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
    fila = {v: (np.nan if _vacio(datos.get(v)) else datos[v]) for v in variables}
    X = pd.DataFrame([fila], columns=variables)
    clase = predecir_con_regla(modelo, X).iloc[0]
    return Prediccion(clase=clase, por_regla=bool(sin_medidas(X).iloc[0]))


def _vacio(valor):
    """Un campo sin rellenar: None, texto vacío o NaN."""
    if valor is None:
        return True
    if isinstance(valor, str):
        return valor.strip() == ""
    return isinstance(valor, float) and np.isnan(valor)
