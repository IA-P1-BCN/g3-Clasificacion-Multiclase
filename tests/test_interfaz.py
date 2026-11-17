"""Tests de la interfaz (app/main.py) con el simulador de Streamlit (AppTest)."""

import pytest
from streamlit.testing.v1 import AppTest

from app.prediccion import ETIQUETAS
from comun import CLASES, MEDIDAS

MEDIDAS_PARCELA = {"DBH": 12.0, "Ht": 9.0}


@pytest.fixture
def app():
    return AppTest.from_file("../app/main.py", default_timeout=60).run()


def numero(app, variable):
    return app.number_input(key=variable)


def texto(elementos):
    return " ".join(str(e.value) for e in elementos)


def test_arranca_sin_errores(app):
    assert not app.exception
    assert app.title[0].value


def test_un_campo_por_variable_con_etiqueta_en_espanol(app):
    etiquetas = {e.label for e in app.number_input} | {e.label for e in app.selectbox}
    for variable in ["DBH", "Ht", *MEDIDAS, "Abbrev"]:
        assert ETIQUETAS[variable] in etiquetas


def test_sin_medidas_responde_none_y_avisa_de_la_regla(app):
    app.selectbox(key="Abbrev").select("Puk")
    for variable, valor in MEDIDAS_PARCELA.items():
        numero(app, variable).set_value(valor)
    app.button[0].click().run()
    assert not app.exception
    assert "none" in texto(app.markdown) + texto(app.subheader)
    assert "regla" in texto(app.info)


def test_valor_imposible_avisa_y_no_predice(app):
    numero(app, "DBH").set_value(-3.0)
    numero(app, "Vig").set_value(3.0)
    app.button[0].click().run()
    assert "Diámetro" in texto(app.error)
    assert not app.subheader


def test_parcela_de_validacion_da_una_de_las_cinco_clases(app):
    ejemplo = app.selectbox(key="ejemplo")
    ejemplo.select(ejemplo.options[1]).run()  # la primera parcela de validación
    assert numero(app, "Vig").value is not None or numero(app, "DBH").value is not None
    app.button[0].click().run()
    assert not app.exception
    resultado = texto(app.subheader)
    assert any(clase in resultado for clase in CLASES)
