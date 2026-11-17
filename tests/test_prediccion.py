"""Tests de la lógica de la app (app/prediccion.py), sin interfaz."""

import pandas as pd
import pytest

from app.prediccion import EntradaInvalida, cargar_modelo, nombre_ganador, predecir
from comun import CLASES, DATOS, MEDIDAS, predecir_con_regla


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


# --- Parcelas sin medidas: `none` por regla fija (ADR-0001) ---------------------


@pytest.mark.parametrize("vacio", [None, ""])
def test_sin_medidas_responde_none_por_regla(modelo, vacio):
    datos = {"Abbrev": "Puk", "DBH": 10.0, "Ht": 8.0, **dict.fromkeys(MEDIDAS, vacio)}
    resultado = predecir(modelo, datos)
    assert resultado.clase == "none"
    assert resultado.por_regla


def test_con_medidas_no_es_por_regla(modelo, val):
    con_medidas = val.dropna(subset=["Vig"]).iloc[0]
    resultado = predecir(modelo, parcela(con_medidas, modelo.feature_names_in_))
    assert not resultado.por_regla


# --- Entrada inválida: error claro y sin predicción --------------------------
@pytest.fixture
def valida(modelo, val):
    return parcela(val.dropna(subset=MEDIDAS).iloc[0], modelo.feature_names_in_)


@pytest.mark.parametrize(
    ("variable", "valor", "texto"),
    [
        ("DBH", -1, "Diámetro"),
        ("DBH", 0, "Diámetro"),
        ("DBH", 250, "Diámetro"),
        ("Ht", 0, "Altura"),
        ("Ht", 61, "Altura"),
        ("Surv", 150, "Supervivencia"),
        ("Surv", -5, "Supervivencia"),
        ("Vig", 7, "Vigor"),
        ("Crown_Fm", -0.5, "copa"),
        ("DBH", "abc", "Diámetro"),
        ("Abbrev", "Marte", "Sitio"),
    ],
)
def test_valor_imposible_da_error_claro(modelo, valida, variable, valor, texto):
    with pytest.raises(EntradaInvalida, match=texto):
        predecir(modelo, {**valida, variable: valor})


def test_avisa_de_todos_los_errores_a_la_vez(modelo, valida):
    with pytest.raises(EntradaInvalida) as error:
        predecir(modelo, {**valida, "DBH": -1, "Vig": 9})
    assert len(error.value.errores) == 2


def test_los_limites_son_validos(modelo, valida):
    limites = {"Surv": 0, "Vig": 5, "Ins_res": 0, "Stem_Fm": 5, "DBH": 200, "Ht": 60}
    assert predecir(modelo, {**valida, **limites}).clase in CLASES
