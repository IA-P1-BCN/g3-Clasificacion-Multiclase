# Acuerdos de ML del grupo

Reglas comunes para que los cuatro modelos sean comparables. Si alguna cambia, se actualiza aquí, en `comun.py` y en el notebook afectado.

## Datos (`01_eda`, sección 10)
La limpieza se hace una sola vez, igual para todos (`01_eda` llama a `limpiar()` de `comun.py`):
1. Split estratificado 70/15/15 con `SEMILLA = 42`, sobre las 736 filas.
2. Solo en **train** se quitan las **parcelas sin medidas** (sin `Surv`, `Vig`, `Ins_res`, `Stem_Fm`, `Crown_Fm` ni `Brnch_Fm`; son los sitios Mor y Wen, todas de clase `none`). Validación y test las conservan. Ver ADR-0001.
3. El diámetro erróneo (`DBH` = 42 085 cm) pasa a NaN en los tres conjuntos y lo imputa el pipeline de cada modelo.
4. Se deja `Abbrev` (el sitio) y se quitan las columnas que solo repiten el sitio: `Locality`, `Map_Ref`, `Latitude`, `Altitude`, `Rainfall`, `Frosts`, `Year`.
5. Se guardan `data/train.csv`, `data/val.csv` y `data/test.csv` (se commitean). Los notebooks de algoritmo solo leen esos CSV.

## Librería común (`comun.py`)
Todo el código que se repite entre notebooks vive en `comun.py`, en la raíz. **Es obligatoria**: los notebooks la importan (`from comun import ...`) y no reescriben sus funciones. Para cambiarla se abre una PR y se avisa al equipo. Lo propio de cada algoritmo (pipeline, rejilla del tuning, interpretación y textos) se queda en su notebook.

| Bloque | Funciones | Quién la usa |
|---|---|---|
| Constantes | `SEMILLA`, `CLASES` (orden `none`…`best`), `MEDIDAS`, `NUMERICAS`, `COLUMNAS_SITIO`, `GAP_MAXIMO` | todos |
| Datos originales | `cargar_openml()`, `dividir()` (split 70/15/15), `sin_medidas()`, `limpiar()`, `guardar_conjuntos()` | `00`, `01` |
| Datos limpios | `cargar_datos()` (train y val; nunca test), `separar_xy()` | `02`–`05` |
| Validación | `cv_comun()`, `cv_por_sitio()`, `f1_por_fold()` (las dos CV), `elegir_sin_sobreajuste()` (refit del `GridSearchCV`) | `02`–`05` |
| Baseline y predicción | `baseline_dummy()`, `predecir_con_regla()` (regla `none`, ADR-0001) | `02`–`06`, app |
| Evaluación | `evaluar_val()` y `mostrar_evaluacion()` (métricas, gap, P/R/F1 por clase, matrices), `nivel_f1()`, `nivel_gap()`, `nivel_baseline()`, `importancia_permutacion()`, `errores_frecuentes()` | `02`–`05` |
| Salida | `guardar_modelo()`, `conclusion_modelo()` (requisitos + resumen), `guardar_resultados()` → `resultados/<notebook>.json`, `cargar_resultados()` | `02`–`05`; `06` |

`final.ipynb` se genera con `python unir_notebooks.py` (orden `00` → `06`) y se commitea en la entrega, después de comprobar que se ejecuta entero.

## Evaluación (notebooks `02`–`05`)
- Validación cruzada común: `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` sobre train.
- Comprobación aparte: `StratifiedGroupKFold` agrupado por `Abbrev`, solo para el informe. Ver ADR-0002.
- **Overfitting**: gap = (F1 macro de train − F1 macro de validación con medidas) × 100, **con signo**. Cumple si es menor de 5 puntos (sobreajuste = train por encima de validación). Si sale por debajo de −5 también cumple, pero `nivel_gap` avisa y hay que comentarlo en el notebook.
- Plantilla común de secciones: preprocesado, CV, métricas en validación (accuracy, precision/recall/F1 por clase, matriz de confusión), gap de overfitting, feature importance (nativa en árbol y regresión logística, `permutation_importance` en SVM y KNN) y análisis de errores.
- El preprocesado lo hace cada persona dentro de su `Pipeline` (ajustado solo con train).
- Las parcelas sin medidas de validación y test **no pasan por el modelo**: se predicen `none` por regla fija antes de calcular las métricas. Las métricas se informan sobre todo el conjunto y también solo sobre las parcelas con medidas.

## Contrato de modelos
- Cada notebook guarda el pipeline completo (preprocesado + modelo) con `joblib` en `models/<notebook>.joblib` (`guardar_modelo`) y sus cifras en `resultados/<notebook>.json` (`conclusion_modelo`). Los dos se commitean.
- **Modelo ganador**: el de mayor F1 macro en **toda la validación** (con la regla `none`) entre los que tienen un gap menor de 5 puntos. `cargar_resultados()` los devuelve ya ordenados así.
- El conjunto de test se usa **una sola vez**, en `06_conclusiones`, con el modelo ganador.

## App (`app/`)
- Streamlit, con la lógica (cargar el pipeline, validar la entrada, predecir) separada de la UI. TDD con pytest en `tests/`.
- Carga `models/<ganador>.joblib`.
- Si la entrada no trae medidas, devuelve `none` por regla fija sin llamar al modelo (ADR-0001), y la app lo indica.
