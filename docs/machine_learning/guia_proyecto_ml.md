# Guía de un proyecto de clasificación en ML

## Vista general

| #  | Paso                              |
| -- | --------------------------------- |
| 0  | Definir el problema               |
| 1  | Datos y split                     |
| 2  | EDA                               |
| 3  | Preprocesado                      |
| 4  | Feature engineering               |
| 5  | Baseline                          |
| 6  | Entrenamiento y validación        |
| 7  | Tuning                            |
| 8  | Evaluación                        |
| 9  | Análisis de errores e interpretación |
| 10 | Despliegue y monitoreo            |

## 0. Definir el problema

Aquí se gana o se pierde el proyecto. Si el problema está mal planteado, un buen modelo no sirve.

### Preguntas

- ¿Qué quiero predecir exactamente? ¿Es binaria, multiclase o multietiqueta?
- ¿Qué decisión se va a tomar con la predicción?
- ¿Qué error cuesta más: un falso positivo o un falso negativo? (Un cáncer no detectado cuesta mucho más que una falsa alarma.)
- ¿Con qué métrica sabré que funciona? ¿Qué resultado cuenta como "suficientemente bueno"?
- ¿Qué haría una persona o una regla simple hoy? Ese es el mínimo a superar.
- ¿Tendré esta información disponible en el momento real de predecir? (Si no, es una trampa.)

## 1. Obtener datos y hacer el split

Haz el split ANTES de explorar a fondo y antes de preprocesar.

### Qué hacer

- Separa en train, validación y test (por ejemplo 70/15/15), o train/test más validación cruzada.
- Usa `stratify=y` para mantener la proporción de clases.
- Si hay tiempo de por medio, parte por fecha, no al azar.
- Si hay varias filas por persona, cliente o paciente, separa por grupo (`GroupKFold`).
- Guarda el test y no lo toques hasta el final.

### Preguntas

- ¿De dónde vienen los datos y quién los generó? ¿Hay sesgos en la recolección?
- ¿Cuántas filas tengo? ¿Alcanzan para el número de variables?
- ¿Hay filas del mismo individuo que puedan filtrarse entre train y test?
- ¿El orden temporal importa?

## 2. EDA (análisis exploratorio)

Solo sobre el set de entrenamiento.

| Qué mirar               | Cómo                        | Pregunta clave                                                                 |
| ----------------------- | --------------------------- | ------------------------------------------------------------------------------ |
| Forma y tipos           | `df.info()`, `df.describe()` | ¿Cada columna tiene el tipo correcto?                                          |
| Variable objetivo       | Conteo de clases            | ¿Está desbalanceada? ¿Cuánto?                                                  |
| Nulos                   | `df.isna().mean()`          | ¿Faltan al azar o hay un patrón? ¿Qué significa un nulo aquí?                  |
| Duplicados              | `df.duplicated().sum()`     | ¿Son errores o repeticiones legítimas?                                         |
| Distribuciones          | Histogramas, boxplots       | ¿Hay asimetría, outliers, valores imposibles?                                  |
| Categóricas             | Conteos, cardinalidad       | ¿Hay categorías raras o escritas distinto ("Madrid", "madrid ")?               |
| Relación con el objetivo | Gráficos por clase         | ¿Qué variables parecen separar las clases?                                     |
| Correlaciones           | Heatmap, VIF                | ¿Hay variables redundantes?                                                    |

### Preguntas

- ¿Algún valor no tiene sentido (edad negativa, fecha futura)?
- ¿Hay columnas que "saben demasiado"? Si una variable predice casi perfecto, sospecha data leakage (por ejemplo, una columna que se llena después del evento).
- ¿Hay columnas inútiles (ID, constantes)?
- ¿Los outliers son errores o casos reales importantes?

## 3. Preprocesado

Regla de oro: ajusta (`fit`) solo con train, aplica (`transform`) a validación y test. Lo más fácil es usar un `Pipeline` con `ColumnTransformer` de scikit-learn, que evita fugas sin esfuerzo.

| Problema           | Opciones                                                                                                              |
| ------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Nulos numéricos    | Mediana, media, KNN imputer                                                                                            |
| Nulos categóricos  | Moda o categoría "desconocido"                                                                                         |
| Categóricas        | One-hot (pocas categorías), ordinal (si hay orden), target encoding (muchas, con cuidado)                              |
| Escala             | `StandardScaler` o `MinMaxScaler` (necesario para regresión logística, SVM, KNN, redes; no para árboles)               |
| Outliers           | Dejarlos, recortar (winsorizing) o transformar con log                                                                 |
| Asimetría          | Log o Box-Cox / Yeo-Johnson                                                                                            |
| Texto o fechas     | Vectorizar (TF-IDF), extraer día, mes, hora                                                                            |

### Preguntas

- ¿Mi modelo necesita este paso o lo maneja solo?
- ¿Estoy ajustando algo con datos que no debería ver (el test)?
- ¿Imputar con la media distorsiona esta variable?

## 4. Feature engineering y selección

### Preguntas

- ¿Qué sabe un experto del dominio que el modelo no puede adivinar? (ratios, diferencias, conteos, antigüedad)
- ¿Puedo combinar variables (precio por metro, ingresos entre deuda)?
- ¿Sobran variables? Quita las constantes, las muy correlacionadas, o usa importancia de variables o regularización L1.
- ¿Cada feature estará disponible al momento de predecir en producción?

## 5. Baseline

Antes de modelos sofisticados, una referencia: un `DummyClassifier` (siempre predice la clase mayoritaria) y una regresión logística simple.

### Preguntas

- ¿Mi modelo complejo supera claramente a esto? Si no, no compensa.
- Si el dummy tiene 95% de accuracy, ¿es que mi problema está desbalanceado y accuracy no sirve?

## 6. Entrenamiento y validación

Prueba varias familias y compara con validación cruzada estratificada (`StratifiedKFold`, 5 folds).

| Modelo                                  | Donde destaca                                  |
| --------------------------------------- | ---------------------------------------------- |
| Regresión logística                     | Baseline, interpretable, datos lineales        |
| Árbol de decisión                       | Interpretable, pero sobreajusta                |
| Random Forest                           | Robusto, poco ajuste                           |
| Gradient Boosting (XGBoost, LightGBM)   | Suele ganar en datos tabulares                 |
| SVM / KNN                               | Datasets pequeños o medianos                   |
| Redes neuronales                        | Imágenes, texto, audio, o muchísimos datos     |

### Desbalance de clases (si aplica), de más simple a más complejo

1. `class_weight="balanced"`.
2. Cambiar el umbral de decisión.
3. Remuestreo (SMOTE, undersampling) solo dentro de cada fold de train, nunca antes del split.

### Preguntas

- ¿La diferencia entre modelos es real o está dentro del ruido de la validación cruzada?
- ¿Hay sobreajuste? (train muy alto, validación mucho más bajo)
- ¿Hay subajuste? (ambos bajos)
- ¿Necesito un modelo explicable por regulación o por confianza del usuario?

## 7. Ajuste de hiperparámetros

`GridSearchCV` (pocos parámetros), `RandomizedSearchCV` u Optuna (muchos). Siempre con validación cruzada, nunca mirando el test.

### Preguntas

- ¿Vale la pena el tiempo? Normalmente el tuning mejora poco comparado con buenos datos y buenas features.
- ¿Estoy sobreajustando a la validación de tanto probar combinaciones?

## 8. Evaluación final

Con el mejor modelo ya elegido, evalúa una sola vez en el test.

| Métrica                | Úsala cuando                                                          |
| ---------------------- | --------------------------------------------------------------------- |
| Accuracy               | Clases balanceadas                                                    |
| Precision              | Los falsos positivos duelen (spam que borra correos buenos)           |
| Recall                 | Los falsos negativos duelen (enfermedad no detectada)                 |
| F1                     | Quieres balance entre precision y recall                              |
| ROC-AUC                | Comparar modelos sin fijar umbral                                     |
| PR-AUC                 | Clases muy desbalanceadas                                             |
| Matriz de confusión    | Siempre, para ver dónde se equivoca                                   |

Además: calibración de probabilidades y elegir el umbral según el costo del error, no dejar 0.5 por defecto.

### Preguntas

- ¿La métrica coincide con lo definido en el paso 0?
- ¿Rinde igual en todos los subgrupos (edad, región, género)? ¿Hay sesgo?
- ¿El resultado en test es parecido al de validación? Si cae mucho, hubo fuga o sobreajuste.

## 9. Análisis de errores e interpretación

- Mira los casos mal clasificados a mano. ¿Tienen algo en común?
- Importancia de variables, SHAP, coeficientes.

### Preguntas

- ¿El modelo se apoya en variables que tienen sentido?
- ¿Aprendió algo absurdo (por ejemplo, el fondo de la imagen en vez del objeto)?
- ¿Qué datos adicionales ayudarían a corregir los errores?

## 10. Despliegue y monitoreo

- Guarda el pipeline completo (preprocesado + modelo) con `joblib`, no solo el modelo.
- Expónlo como API, batch o app.
- Vigila el data drift (los datos cambian) y el rendimiento en el tiempo.

### Preguntas

- ¿Cómo sabré que el modelo empezó a fallar?
- ¿Cada cuánto hay que reentrenar?
- ¿Qué pasa si el modelo se equivoca? ¿Hay revisión humana?

## Los 5 errores más comunes

1. Preprocesar antes del split (fuga de datos).
2. Usar accuracy con clases desbalanceadas.
3. Hacer SMOTE antes de la validación cruzada.
4. Mirar el test para tomar decisiones.
5. No definir qué error cuesta más antes de empezar.
