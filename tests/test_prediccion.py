"""Tests de la lógica de la app (app/prediccion.py), sin interfaz."""

import pandas as pd
import pytest

from app.prediccion import cargar_modelo, nombre_ganador, predecir
from comun import CLASES, DATOS, predecir_con_regla


@pytest.fixture(scope="module")
def modelo():
    return cargar_modelo()


@pytest.fixture(scope="module")
def val():
    return pd.read_csv(DATOS / "val.csv", encoding="utf-8")


def parcela(fila, variables):
    """Una fila de validación como la rellenaría el formulario (NaN → None)."""
    return {v: (None if pd.isna(fila[v]) else fila[v]) for v in variables}


def test_el_ganador_es_el_elegido_en_06():
    assert nombre_ganador() == "04_svm"


def test_predice_una_de_las_cinco_clases(modelo, val):
    con_medidas = val.dropna(subset=["Vig"]).iloc[0]
    resultado = predecir(modelo, parcela(con_medidas, modelo.feature_names_in_))
    assert resultado.clase in CLASES
    assert not resultado.por_regla


def test_coincide_con_el_notebook_en_toda_la_validacion(modelo, val):
    variables = list(modelo.feature_names_in_)
    esperado = predecir_con_regla(modelo, val[variables])
    obtenido = [predecir(modelo, parcela(f, variables)).clase for _, f in val.iterrows()]
    assert obtenido == list(esperado)
