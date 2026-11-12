# Acuerdos de ML del grupo

Reglas comunes para que los cuatro modelos sean comparables. Si alguna cambia, se actualiza aquí y en el notebook afectado.

## Datos (`01_eda`)
Al final del EDA, la limpieza se aplica una sola vez y con la misma regla a train, validación y test:
1. Se quitan las **parcelas sin medidas** (sin `Surv`, `Vig`, `Ins_res`, `Stem_Fm`, `Crown_Fm` ni `Brnch_Fm`; son los sitios Mor y Wen, todas de clase `none`). Ver ADR-0001.
2. El diámetro erróneo (`DBH` = 42 085 cm) pasa a NaN y lo imputa el pipeline de cada modelo.
3. Se deja `Abbrev` (el sitio) y se quitan las columnas que solo repiten el sitio: `Locality`, `Map_Ref`, `Latitude`, `Altitude`, `Rainfall`, `Frosts`, `Year`.
4. El split es el del principio del EDA: estratificado 70/15/15 con `SEMILLA = 42`.
5. Se guardan `data/train.csv`, `data/val.csv` y `data/test.csv` (se commitean). Los notebooks de algoritmo solo leen esos CSV.

No hay un `src/` compartido: el código de la limpieza vive únicamente en `01_eda`.

## Evaluación (notebooks `02`–`05`)
- Validación cruzada común: `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` sobre train.
- Comprobación aparte: `StratifiedGroupKFold` agrupado por `Abbrev`, solo para el informe. Ver ADR-0002.
- **Overfitting**: diferencia de **F1 macro** entre train y validación, por debajo de 5 puntos.
- Plantilla común de secciones: preprocesado, CV, métricas en validación (accuracy, precision/recall/F1 por clase, matriz de confusión), gap de overfitting, feature importance (nativa en árbol y regresión logística, `permutation_importance` en SVM y KNN) y análisis de errores.
- El preprocesado lo hace cada persona dentro de su `Pipeline` (ajustado solo con train).

## Contrato de modelos
- Cada notebook guarda el pipeline completo (preprocesado + modelo) con `joblib` en `models/<algoritmo>.joblib` (se commitea).
- **Modelo ganador**: el de mayor F1 macro en validación entre los que tienen un gap menor de 5 puntos.
- El conjunto de test se usa **una sola vez**, en `06_conclusiones`, con el modelo ganador.

## App (`app/`)
- Streamlit, con la lógica (cargar el pipeline, validar la entrada, predecir) separada de la UI. TDD con pytest en `tests/`.
- Carga `models/<ganador>.joblib`.
- Si la entrada no trae medidas, devuelve `none` por regla fija sin llamar al modelo (ADR-0001), y la app lo indica.
