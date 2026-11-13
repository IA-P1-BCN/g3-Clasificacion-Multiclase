"""Librería común del equipo g3 (dataset Eucalyptus, objetivo `Utility`).

Todos los notebooks la importan (`from comun import ...`). Así todos cargamos,
limpiamos, validamos, evaluamos y guardamos igual. Las reglas que aplica están en
`docs/acuerdos.md` y en los ADR de `docs/adr/`. Si hace falta cambiar algo, se
cambia aquí, por PR y avisando al equipo, nunca copiando la función en un notebook.

Índice
- Constantes ................ SEMILLA, CLASES, MEDIDAS, NUMERICAS, GAP_MAXIMO...
- Datos originales (00, 01) . cargar_openml, dividir, sin_medidas, limpiar,
                              guardar_conjuntos
- Datos limpios (02-05) ..... cargar_datos, separar_xy
- Validación ................ cv_comun, cv_por_sitio, f1_por_fold,
                              elegir_sin_sobreajuste
- Baseline y predicción ..... baseline_dummy, predecir_con_regla
- Evaluación ................ nivel_f1, nivel_gap, nivel_baseline, evaluar_val,
                              mostrar_evaluacion, por_clase, dibujar_matriz,
                              importancia_permutacion, errores_frecuentes
- Salida .................... guardar_modelo, conclusion_modelo, guardar_resultados,
                              cargar_resultados
"""

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.datasets import fetch_openml
from sklearn.dummy import DummyClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import (
    StratifiedGroupKFold,
    StratifiedKFold,
    cross_validate,
    train_test_split,
)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "data"
MODELOS = RAIZ / "models"
RESULTADOS = RAIZ / "resultados"

SEMILLA = 42
OBJETIVO = "Utility"
# Escala ordenada de peor a mejor: es el orden de todas las tablas y matrices
CLASES = ["none", "low", "average", "good", "best"]
# Si faltan TODAS estas medidas, la parcela no se mide (ADR-0001)
MEDIDAS = ["Surv", "Vig", "Ins_res", "Stem_Fm", "Crown_Fm", "Brnch_Fm"]
NUMERICAS = ["DBH", "Ht", *MEDIDAS]
# Columnas que solo repiten el sitio (`Abbrev`): se quitan en la limpieza
COLUMNAS_SITIO = [
    "Locality",
    "Map_Ref",
    "Latitude",
    "Altitude",
    "Rainfall",
    "Frosts",
    "Year",
]
# Overfitting: F1 macro de train menos F1 macro de validación, en puntos (0-100)
GAP_MAXIMO = 5


# ---------------------------------------------------------------------------
# Datos originales (00_general y 01_eda)
# ---------------------------------------------------------------------------
def cargar_openml():
    """Descarga Eucalyptus (OpenML 188) y devuelve X, y. Se guarda en caché local."""
    datos = fetch_openml(data_id=188, as_frame=True)
    return datos.data, datos.target


def dividir(X, y):
    """Split estratificado 70/15/15 con SEMILLA.

    Devuelve X_train, X_val, X_test, y_train, y_val, y_test.
    """
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=SEMILLA
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=SEMILLA
    )
    return X_train, X_val, X_test, y_train, y_val, y_test


def sin_medidas(X):
    """True en las parcelas a las que les faltan TODAS las MEDIDAS (ADR-0001)."""
    return X[MEDIDAS].isna().all(axis=1)


def limpiar(X, y, quitar_sin_medidas):
    """Limpieza común (docs/acuerdos.md § Datos).

    Quita COLUMNAS_SITIO, pone a NaN el DBH erróneo (> 1000 cm) y, solo si
    `quitar_sin_medidas` (en train), quita las parcelas sin medidas.
    """
    df = X.drop(columns=COLUMNAS_SITIO).assign(**{OBJETIVO: y})
    # 42085 cm es un error evidente: un árbol no mide 420 m de diámetro
    df.loc[df["DBH"] > 1000, "DBH"] = np.nan
    if quitar_sin_medidas:
        df = df[~sin_medidas(X)]
    return df


def guardar_conjuntos(conjuntos):
    """Guarda cada DataFrame de {"train": df, ...} en data/<nombre>.csv y .joblib."""
    DATOS.mkdir(exist_ok=True)
    for nombre, df in conjuntos.items():
        joblib.dump(df, DATOS / f"{nombre}.joblib")
        df.to_csv(DATOS / f"{nombre}.csv", index=False, encoding="utf-8")
        print(f"{nombre}: {df.shape[0]} filas, {df.shape[1]} columnas")


# ---------------------------------------------------------------------------
# Datos limpios (notebooks de algoritmo)
# ---------------------------------------------------------------------------
def cargar_datos():
    """Lee data/train.csv y data/val.csv. El test no se lee aquí: solo en 06."""
    train = pd.read_csv(DATOS / "train.csv", encoding="utf-8")
    val = pd.read_csv(DATOS / "val.csv", encoding="utf-8")
    return train, val


def separar_xy(df, variables=None):
    """Devuelve X (las `variables` elegidas, o todas menos el objetivo) e y."""
    X = df.drop(columns=OBJETIVO) if variables is None else df[variables]
    return X, df[OBJETIVO]


# ---------------------------------------------------------------------------
# Validación
# ---------------------------------------------------------------------------
def cv_comun():
    """StratifiedKFold de 5 folds común a todos (docs/acuerdos.md)."""
    return StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA)


def cv_por_sitio():
    """StratifiedGroupKFold por sitio (`Abbrev`): solo para el informe (ADR-0002)."""
    return StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEMILLA)


def f1_por_fold(modelo, X, y):
    """F1 macro de cada fold con las dos validaciones cruzadas.

    Muestra la tabla de folds y devuelve un dict con medias, desviaciones,
    el F1 de train de la CV común y su gap (en puntos).
    """
    comun = cross_validate(
        modelo,
        X,
        y,
        cv=cv_comun(),
        scoring="f1_macro",
        return_train_score=True,
        n_jobs=-1,
    )
    sitio = cross_validate(
        modelo,
        X,
        y,
        cv=cv_por_sitio(),
        groups=X["Abbrev"],
        scoring="f1_macro",
        return_train_score=True,
        n_jobs=-1,
    )
    folds = pd.DataFrame(
        {
            "fold": range(1, 6),
            "StratifiedKFold": comun["test_score"],
            "por sitio (StratifiedGroupKFold)": sitio["test_score"],
        }
    ).set_index("fold")
    display(folds.round(3))
    cv = {
        "f1": comun["test_score"].mean(),
        "desv": comun["test_score"].std(),
        "f1_train": comun["train_score"].mean(),
        "f1_sitio": sitio["test_score"].mean(),
        "desv_sitio": sitio["test_score"].std(),
        "gap_sitio": 100 * (sitio["train_score"].mean() - sitio["test_score"].mean()),
    }
    cv["gap"] = 100 * (cv["f1_train"] - cv["f1"])
    print(
        f"StratifiedKFold: F1 macro = {cv['f1']:.3f} ± {cv['desv']:.3f} "
        f"| gap {cv['gap']:.1f} puntos {nivel_gap(cv['gap'])}"
    )
    print(
        f"Por sitio:       F1 macro = {cv['f1_sitio']:.3f} ± {cv['desv_sitio']:.3f} "
        f"| gap {cv['gap_sitio']:.1f} puntos"
    )
    return cv


def elegir_sin_sobreajuste(cv_results, desempate=None):
    """Regla de elección para `GridSearchCV(refit=...)`.

    Entre las combinaciones con gap (train - CV) < GAP_MAXIMO, la de mayor F1 en
    CV. `desempate` = lista de (columna de cv_results, ascendente) para elegir
    entre empates, p. ej. [("param_arbol__max_depth", True)]. Si ninguna cumple,
    se queda con la de menor gap y avisa.

    Uso: `GridSearchCV(..., return_train_score=True,
    refit=lambda r: elegir_sin_sobreajuste(r, desempate))`.
    """
    r = pd.DataFrame(cv_results)
    r["gap"] = 100 * (r["mean_train_score"] - r["mean_test_score"])
    candidatos = r[r["gap"] < GAP_MAXIMO]
    if candidatos.empty:
        print(
            f"⚠️ Ninguna combinación tiene gap < {GAP_MAXIMO}: se elige la de menor gap."
        )
        return int(r["gap"].idxmin())
    columnas, ascendente = ["mean_test_score"], [False]
    for columna, asc in desempate or []:
        columnas.append(columna)
        ascendente.append(asc)
    ordenados = candidatos.sort_values(
        columnas, ascending=ascendente, na_position="last"
    )
    return int(ordenados.index[0])


# ---------------------------------------------------------------------------
# Baseline y predicción
# ---------------------------------------------------------------------------
def predecir_con_regla(modelo, X):
    """Predice con el modelo y responde `none` a las parcelas sin medidas (ADR-0001)."""
    con_medidas = ~sin_medidas(X)
    prediccion = pd.Series("none", index=X.index, name="predicha", dtype=object)
    if con_medidas.any():
        prediccion.loc[con_medidas] = modelo.predict(X.loc[con_medidas])
    return prediccion


def baseline_dummy(X_train, y_train, X_val, y_val):
    """Dummy (siempre la clase más frecuente): el mínimo que hay que superar.

    Devuelve el F1 macro en CV, en toda la validación (con la regla) y solo en las
    parcelas con medidas. Sale igual en todos los notebooks.
    """
    dummy = DummyClassifier(strategy="most_frequent")
    r = cross_validate(
        dummy, X_train, y_train, cv=cv_comun(), scoring=["f1_macro", "accuracy"]
    )
    dummy.fit(X_train, y_train)
    pred = predecir_con_regla(dummy, X_val)
    medidas = ~sin_medidas(X_val)
    f1 = {
        "cv": r["test_f1_macro"].mean(),
        "toda la validación": f1_score(y_val, pred, average="macro"),
        "solo con medidas": f1_score(y_val[medidas], pred[medidas], average="macro"),
    }
    print(
        f"El Dummy responde siempre «{dummy.classes_[np.argmax(dummy.class_prior_)]}» "
        "(y «none» a las parcelas sin medidas, por la regla)."
    )
    display(
        pd.DataFrame(
            {
                "F1 macro": f1,
                "accuracy": {
                    "cv": r["test_accuracy"].mean(),
                    "toda la validación": accuracy_score(y_val, pred),
                    "solo con medidas": accuracy_score(y_val[medidas], pred[medidas]),
                },
            }
        ).round(3)
    )
    return f1


# ---------------------------------------------------------------------------
# Evaluación
# ---------------------------------------------------------------------------
def nivel_f1(f1):
    """Nivel del F1 macro (0-1)."""
    if f1 < 0.30:
        return "❌ malo"
    if f1 < 0.50:
        return "⚠️ flojo"
    if f1 < 0.70:
        return "✅ aceptable"
    return "🌟 bueno"


def nivel_gap(gap):
    """Nivel del gap en puntos, con signo (train - validación).

    Cumple si gap < GAP_MAXIMO. Por debajo de -GAP_MAXIMO también cumple, pero se
    avisa: validación sale mucho más alta que train y hay que comentarlo.
    """
    if gap < -GAP_MAXIMO:
        return "✅ cumple (⚠️ validación mucho más alta que train)"
    if gap < GAP_MAXIMO:
        return "✅ correcto"
    if gap < 2 * GAP_MAXIMO:
        return "❌ ligero sobreajuste"
    return "❌ sobreajuste grave"


def nivel_baseline(puntos):
    """Cuánto supera al Dummy, en puntos de F1 macro."""
    if puntos < 10:
        return "❌ no supera"
    if puntos < 25:
        return "⚠️ supera poco"
    return "✅ supera claramente"


def ok(condicion):
    return "✅" if condicion else "❌"


def evaluar_val(modelo, X_train, y_train, X_val, y_val, dummy):
    """Evalúa el modelo (ya entrenado) en validación, con la regla `none`.

    Calcula las métricas en toda la validación y solo con medidas, y el gap
    (train - validación con medidas, con signo, en puntos). `dummy` es lo que
    devuelve baseline_dummy. Devuelve un dict que usan mostrar_evaluacion,
    conclusion_modelo y guardar_resultados.
    """
    pred = predecir_con_regla(modelo, X_val)
    medidas = ~sin_medidas(X_val)
    f1_train = f1_score(y_train, modelo.predict(X_train), average="macro")
    filas = {}
    for conjunto, (y, p) in {
        "toda la validación": (y_val, pred),
        "solo con medidas": (y_val[medidas], pred[medidas]),
    }.items():
        f1 = f1_score(y, p, average="macro")
        filas[conjunto] = {
            "F1 macro": f1,
            "nivel F1": nivel_f1(f1),
            "supera Dummy (puntos)": 100 * (f1 - dummy[conjunto]),
            "nivel baseline": nivel_baseline(100 * (f1 - dummy[conjunto])),
            "accuracy": accuracy_score(y, p),
            "accuracy balanceada": balanced_accuracy_score(y, p),
            "precision macro": precision_score(y, p, average="macro", zero_division=0),
            "recall macro": recall_score(y, p, average="macro", zero_division=0),
            "F1 ponderado": f1_score(y, p, average="weighted"),
        }
    gap = 100 * (f1_train - filas["solo con medidas"]["F1 macro"])
    return {
        "y": y_val,
        "pred": pred,
        "medidas": medidas,
        "f1_train": f1_train,
        "gap": gap,
        "cumple_gap": gap < GAP_MAXIMO,
        "filas": filas,
    }


def por_clase(y, pred):
    """Precision, recall, F1 y soporte de cada clase, en el orden de CLASES."""
    informe = classification_report(
        y, pred, labels=CLASES, output_dict=True, zero_division=0
    )
    return (
        pd.DataFrame(informe)
        .T.loc[CLASES]
        .rename(columns={"f1-score": "f1", "support": "soporte"})
    )


def dibujar_matriz(y, pred, titulo, ax=None):
    """Matriz de confusión con filas (real) y columnas (predicha) en orden CLASES."""
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4.8))
    ConfusionMatrixDisplay.from_predictions(
        y, pred, labels=CLASES, ax=ax, colorbar=False, cmap="Blues"
    )
    ax.set(title=titulo, xlabel="Clase predicha", ylabel="Clase real")
    return ax


def mostrar_evaluacion(ev):
    """Las salidas que pide el enunciado, siempre en el mismo orden.

    1. métricas globales, 2. gap de overfitting, 3. P/R/F1 por clase,
    4. matrices de confusión (toda la validación y solo con medidas).
    """
    print("1. MÉTRICAS EN VALIDACIÓN")
    display(pd.DataFrame.from_dict(ev["filas"], orient="index").round(3))
    print(
        f"2. OVERFITTING: F1 train {ev['f1_train']:.3f} - F1 validación con medidas "
        f"{ev['filas']['solo con medidas']['F1 macro']:.3f} = {ev['gap']:.1f} puntos "
        f"→ {nivel_gap(ev['gap'])}"
    )
    print("3. MÉTRICAS POR CLASE")
    y, pred, m = ev["y"], ev["pred"], ev["medidas"]
    display(
        pd.concat(
            {
                "toda la validación": por_clase(y, pred),
                "solo con medidas": por_clase(y[m], pred[m]),
            },
            axis=1,
        ).round(2)
    )
    print("4. MATRICES DE CONFUSIÓN")
    _, ejes = plt.subplots(1, 2, figsize=(12, 4.8))
    dibujar_matriz(y, pred, "Toda la validación (con la regla)", ejes[0])
    dibujar_matriz(y[m], pred[m], "Solo parcelas con medidas", ejes[1])
    plt.tight_layout()
    plt.show()


def importancia_permutacion(modelo, X_val, y_val, n_repeats=10):
    """Importancia por permutación (caída del F1 macro), igual para cualquier modelo.

    Se calcula solo con las parcelas con medidas, que son las que ve el modelo.
    Devuelve la Serie ordenada y dibuja las barras.
    """
    m = ~sin_medidas(X_val)
    r = permutation_importance(
        modelo,
        X_val[m],
        y_val[m],
        scoring="f1_macro",
        n_repeats=n_repeats,
        random_state=SEMILLA,
        n_jobs=-1,
    )
    importancia = pd.Series(r.importances_mean, index=X_val.columns).sort_values()
    ax = importancia.plot.barh(figsize=(8, 4.5), color="steelblue")
    ax.set(
        xlabel="Caída del F1 macro al desordenar la variable",
        title="Importancia por permutación (validación con medidas)",
    )
    plt.show()
    return importancia


def errores_frecuentes(y, pred, n=10):
    """Tabla de confusiones (real → predicha) ordenadas de más a menos frecuente.

    `distancia` = cuántas clases separan la real de la predicha en la escala;
    a partir de 2 es un error grave.
    """
    posicion = {c: i for i, c in enumerate(CLASES)}
    errores = pd.DataFrame({"real": y, "predicha": pred})[y != pred]
    tabla = errores.value_counts().rename("parcelas").reset_index()
    tabla["distancia"] = (
        tabla["real"].map(posicion) - tabla["predicha"].map(posicion)
    ).abs()
    graves = tabla.loc[tabla["distancia"] >= 2, "parcelas"].sum()
    print(
        f"Errores: {len(errores)} de {len(y)}. Entre clases vecinas: "
        f"{len(errores) - graves}; a 2 o más clases de distancia: {graves}."
    )
    return tabla.head(n)


# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------
def guardar_modelo(modelo, nombre, X_val):
    """Guarda el pipeline en models/<nombre>.joblib y comprueba que se recarga.

    `nombre` es el del notebook (p. ej. "03_arbol_decision"). Devuelve la ruta.
    """
    MODELOS.mkdir(exist_ok=True)
    ruta = MODELOS / f"{nombre}.joblib"
    joblib.dump(modelo, ruta)
    iguales = (
        predecir_con_regla(joblib.load(ruta), X_val)
        == predecir_con_regla(modelo, X_val)
    ).all()
    print(
        f"Guardado: {ruta.relative_to(RAIZ)} ({ruta.stat().st_size / 1024:.1f} KB). "
        f"¿Al recargarlo predice igual? {ok(iguales)}"
    )
    return ruta


def guardar_resultados(nombre, cv, ev, hiperparametros):
    """Escribe resultados/<nombre>.json con lo que 06_conclusiones necesita."""
    RESULTADOS.mkdir(exist_ok=True)
    m = ev["medidas"]
    resultado = {
        "modelo": nombre,
        "hiperparametros": {
            k: (v if isinstance(v, (int, float, str, bool)) or v is None else str(v))
            for k, v in hiperparametros.items()
        },
        "f1_cv": cv["f1"],
        "desv_cv": cv["desv"],
        "gap_cv": cv["gap"],
        "f1_cv_sitio": cv["f1_sitio"],
        "desv_cv_sitio": cv["desv_sitio"],
        "f1_train": ev["f1_train"],
        "f1_val": ev["filas"]["toda la validación"]["F1 macro"],
        "f1_val_medidas": ev["filas"]["solo con medidas"]["F1 macro"],
        "gap": ev["gap"],
        "cumple_gap": bool(ev["cumple_gap"]),
        "metricas": {
            conjunto: {k: v for k, v in fila.items() if not k.startswith("nivel")}
            for conjunto, fila in ev["filas"].items()
        },
        "por_clase": {
            "toda la validación": por_clase(ev["y"], ev["pred"]).to_dict(
                orient="index"
            ),
            "solo con medidas": por_clase(ev["y"][m], ev["pred"][m]).to_dict(
                orient="index"
            ),
        },
    }
    ruta = RESULTADOS / f"{nombre}.json"
    ruta.write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2, default=float),
        encoding="utf-8",
    )
    print(f"Resultados guardados en {ruta.relative_to(RAIZ)}")
    return ruta


def conclusion_modelo(nombre, cv, ev, dummy, hiperparametros):
    """Conclusión común: tabla de requisitos, resumen y resultados/<nombre>.json.

    Los requisitos que no se comprueban con código (feature importance, análisis de
    errores, preprocesado dentro del Pipeline) se rellenan en el texto de después.
    """
    medidas = ev["filas"]["solo con medidas"]
    ruta_modelo = MODELOS / f"{nombre}.joblib"
    requisitos = pd.DataFrame(
        [
            (
                "R1",
                "Multiclase (≥ 3 clases)",
                "Enunciado",
                f"{ev['y'].nunique()} clases",
                ok(ev["y"].nunique() >= 3),
            ),
            (
                "R2",
                f"Overfitting < {GAP_MAXIMO} puntos (train - validación con medidas)",
                "Enunciado",
                f"{ev['gap']:.1f} puntos",
                ok(ev["cumple_gap"]),
            ),
            (
                "R3",
                "Supera claramente al Dummy (validación con medidas)",
                "Guía, paso 5",
                f"{medidas['supera Dummy (puntos)']:+.0f} puntos",
                ok(medidas["supera Dummy (puntos)"] >= 25),
            ),
            (
                "R4",
                "Sin medidas → none por regla; métricas con y sin",
                "ADR-0001",
                f"{(~ev['medidas']).sum()} parcelas",
                ok((ev["pred"][~ev["medidas"]] == "none").all()),
            ),
            (
                "R5",
                "StratifiedKFold + comprobación por sitio",
                "ADR-0002",
                f"{cv['f1']:.3f} / {cv['f1_sitio']:.3f}",
                "✅",
            ),
            (
                "R6",
                "Pipeline guardado",
                "Acuerdos",
                f"models/{nombre}.joblib",
                ok(ruta_modelo.exists()),
            ),
        ],
        columns=["id", "requisito", "fuente", "resultado", "cumple"],
    ).set_index("id")
    display(requisitos)
    toda = ev["filas"]["toda la validación"]
    display(
        pd.DataFrame(
            {
                "validación cruzada": [
                    cv["f1"],
                    cv["gap"],
                    100 * (cv["f1"] - dummy["cv"]),
                ],
                "validación con regla": [
                    toda["F1 macro"],
                    np.nan,
                    toda["supera Dummy (puntos)"],
                ],
                "validación solo con medidas": [
                    medidas["F1 macro"],
                    ev["gap"],
                    medidas["supera Dummy (puntos)"],
                ],
            },
            index=["F1 macro", "gap (puntos)", "supera Dummy (puntos)"],
        ).round(3)
    )
    return guardar_resultados(nombre, cv, ev, hiperparametros)


def cargar_resultados():
    """Para 06_conclusiones: tabla con los resultados/*.json de todos los modelos.

    Ordenada según la regla del ganador: primero los que cumplen el gap y, entre
    ellos, el de mayor F1 macro en toda la validación (docs/acuerdos.md).
    """
    filas = [
        json.loads(ruta.read_text(encoding="utf-8"))
        for ruta in sorted(RESULTADOS.glob("*.json"))
    ]
    columnas = [
        "modelo",
        "f1_cv",
        "desv_cv",
        "f1_cv_sitio",
        "f1_train",
        "f1_val",
        "f1_val_medidas",
        "gap",
        "cumple_gap",
    ]
    tabla = pd.DataFrame(filas, columns=columnas)
    return tabla.sort_values(
        ["cumple_gap", "f1_val"], ascending=[False, False]
    ).set_index("modelo")
