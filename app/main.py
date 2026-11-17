"""Interfaz Streamlit: predice la clase de utilidad de una parcela de eucalipto.

Arranque, desde la raíz del repo: streamlit run app/main.py
La lógica (modelo, validación y regla `none`) está en app/prediccion.py.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:  # para importar `app` y `comun` desde la raíz
    sys.path.insert(0, str(RAIZ))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from app.prediccion import (  # noqa: E402
    ETIQUETAS,
    SITIO_DESCONOCIDO,
    SITIOS,
    EntradaInvalida,
    cargar_modelo,
    nombre_ganador,
    predecir,
)
from comun import CLASES, DATOS, MEDIDAS, cargar_resultados  # noqa: E402

SIGNIFICADO = {
    "none": "No sirve para conservar el suelo.",
    "low": "Utilidad baja para conservar el suelo.",
    "average": "Utilidad media para conservar el suelo.",
    "good": "Buena utilidad para conservar el suelo.",
    "best": "La mejor utilidad para conservar el suelo.",
}
AYUDA = {
    "DBH": "Diámetro medio del tronco a la altura del pecho, en centímetros.",
    "Ht": "Altura media de los árboles, en metros.",
    "Surv": "Porcentaje de árboles que sobreviven en la parcela.",
    "Vig": "Puntuación del crecimiento de los árboles, de 0 a 5.",
    "Ins_res": "Puntuación de la resistencia a insectos, de 0 a 5.",
    "Stem_Fm": "Puntuación de la forma del tronco, de 0 a 5.",
    "Crown_Fm": "Puntuación de la forma de la copa, de 0 a 5.",
    "Brnch_Fm": "Puntuación de la forma de las ramas, de 0 a 5.",
}


@st.cache_resource
def modelo_ganador():
    nombre = nombre_ganador()
    return nombre, cargar_modelo(nombre)


@st.cache_data
def parcelas_de_validacion():
    return pd.read_csv(DATOS / "val.csv", encoding="utf-8")


def rellenar_con_ejemplo():
    """Copia en el formulario los datos de la parcela de validación elegida."""
    i = st.session_state["ejemplo"]
    if i is None:
        return
    fila = parcelas_de_validacion().loc[i]
    for variable in variables:
        valor = fila[variable]
        if variable == "Abbrev":
            st.session_state[variable] = valor
        else:
            st.session_state[variable] = None if pd.isna(valor) else float(valor)


st.set_page_config(page_title="Utilidad de una parcela de eucalipto", page_icon="🌳")
st.title("🌳 Utilidad de una parcela de eucalipto")
st.write(
    "Introduce los datos de una parcela de ensayo y la app predice su **clase de "
    "utilidad para conservar el suelo**: `none` < `low` < `average` < `good` < "
    "`best`. Los campos vacíos se pueden dejar en blanco."
)

nombre, modelo = modelo_ganador()
variables = list(modelo.feature_names_in_)
val = parcelas_de_validacion()

st.selectbox(
    "Rellenar con una parcela de validación (opcional)",
    options=[None, *val.index],
    format_func=lambda i: (
        "—" if i is None else f"Parcela {i} · sitio {val.at[i, 'Abbrev']}"
    ),
    key="ejemplo",
    on_change=rellenar_con_ejemplo,
)

with st.form("parcela"):
    st.markdown("#### Sitio y tamaño")
    st.selectbox(
        ETIQUETAS["Abbrev"],
        options=[*SITIOS, SITIO_DESCONOCIDO],
        index=None,
        placeholder="Elige el sitio",
        key="Abbrev",
    )
    izquierda, derecha = st.columns(2)
    numericas = [v for v in variables if v != "Abbrev"]
    for posicion, variable in enumerate(numericas):
        if variable == MEDIDAS[0]:
            st.markdown("#### Medidas de la parcela")
            st.caption(
                "Si dejas vacías **todas** las medidas, la app responde `none` "
                "por una regla fija."
            )
        columna = izquierda if posicion % 2 == 0 else derecha
        columna.number_input(
            ETIQUETAS.get(variable, variable),
            value=None,
            step=0.1,
            format="%.2f",
            help=AYUDA.get(variable),
            key=variable,
        )
    enviado = st.form_submit_button("Predecir", type="primary")

if enviado:
    datos = {v: st.session_state.get(v) for v in variables}
    try:
        resultado = predecir(modelo, datos)
    except EntradaInvalida as error:
        st.error(
            "**No se puede predecir: hay datos imposibles.**\n\n"
            + "\n".join(f"- {mensaje}" for mensaje in error.errores)
        )
        st.stop()

    st.subheader(f"Clase de utilidad: {resultado.clase}")
    escala = " < ".join(f"**[{c}]**" if c == resultado.clase else c for c in CLASES)
    st.markdown(f"{escala}\n\n{SIGNIFICADO[resultado.clase]}")

    if resultado.por_regla:
        st.info(
            "Es una **parcela sin medidas**: la respuesta `none` sale de una "
            "**regla fija**, no del modelo. En los datos del ensayo, todas las "
            "parcelas sin medidas son `none` (ADR-0001)."
        )
    else:
        if resultado.faltan:
            faltan = ", ".join(ETIQUETAS.get(v, v) for v in resultado.faltan)
            st.warning(
                f"Faltan datos: {faltan}. El modelo los completa con el valor "
                "típico (la mediana) de las parcelas de entrenamiento, así que la "
                "predicción es menos segura."
            )
        if not resultado.sitio_conocido:
            st.warning(
                "El modelo no vio este sitio al entrenar. En sitios nuevos acierta "
                "menos (F1 macro ≈ 0.51 frente a 0.58 en la validación cruzada)."
            )
    if st.session_state.get("ejemplo") is not None:
        real = val.at[st.session_state["ejemplo"], "Utility"]
        st.caption(
            f"Clase real de la parcela de ejemplo: **{real}** (si no has cambiado "
            "sus datos)."
        )

with st.expander("Sobre el modelo"):
    resumen = cargar_resultados().loc[nombre]
    st.markdown(
        f"Modelo ganador: **{nombre}** (`models/{nombre}.joblib`), elegido en "
        "`06_conclusiones` por tener el mayor F1 macro en validación entre los "
        f"modelos sin sobreajuste. F1 macro en validación: **{resumen['f1_val']:.3f}**;"
        f" gap de sobreajuste: {resumen['gap']:.1f} puntos. Cuando se equivoca, casi "
        "siempre confunde clases vecinas (por ejemplo, `best` con `good`)."
    )
