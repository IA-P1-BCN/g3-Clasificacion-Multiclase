# Reparto de la presentación entre cuatro personas

Propuesta para la presentación completa ([`presentacion-eucalyptus.html`](presentacion-eucalyptus.html), 25 diapositivas: negocio, app y código). Duración orientativa: unos 37 minutos. El reparto sigue quién hizo cada parte según el historial del repositorio; se puede cambiar de común acuerdo.

## Resumen

| Persona | Diapositivas | Qué cuenta | Tiempo | Apoyo para las preguntas |
|---|---|---|---|---|
| **Fabiana** (regresión logística) | 1 a 5, 17 y 25 | Abre con la historia de negocio y cierra con los siguientes pasos | ≈ 8 min | [`modelos/regresion-logistica.html`](modelos/regresion-logistica.html) |
| **Jc** (app, árbol de decisión, estructura del código) | 6 a 9, 18 y 24 | Límites del modelo, demo de la app, estructura del código y errores | ≈ 10,5 min | [`modelos/arbol-decision.html`](modelos/arbol-decision.html) |
| **Manon** (EDA y KNN) | 10 a 14 y 20 | De los datos a la validación: EDA, decisiones, limpieza, variables y split | ≈ 9,5 min | [`modelos/knn.html`](modelos/knn.html) |
| **Elena** (SVM e informe técnico) | 15, 16, 19 y 21 a 23 | Los cuatro modelos, la comparación, el ganador y el test | ≈ 9 min | [`modelos/svm.html`](modelos/svm.html) |

## Por qué así

- **Cada persona presenta su propio modelo** (diapositivas 17 a 20): es lo que mejor sabe contar y lo que más preguntas va a recibir.
- **Fabiana abre y cierra:** la historia de negocio y los siguientes pasos no necesitan jerga, y el cierre recoge negocio y código.
- **Jc lleva la demo** porque construyó la app y sus tests, y también la estructura del código.
- **Manon lleva la parte de datos** (EDA, limpieza y validación) y cuenta el KNN, el modelo cuyo resultado hay que explicar con más cuidado.
- **Elena lleva la decisión final:** el SVM es el ganador y ella redactó el informe técnico.

## Orden de intervención

### Negocio

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 1 | Portada | Fabiana | Qué se va a contar y en qué orden: negocio, app y código | 0,5 |
| 2 | El problema | Fabiana | 736 parcelas en 16 sitios; calificación de none a best | 1 |
| 3 | La solución | Fabiana | El modelo repite la calificación a partir de las medidas. No se prueba si el eucalipto mejora el suelo | 1,5 |
| 4 | El resultado | Fabiana | Acierta unas 7 de cada 10 parcelas; 34 de los 35 errores son de un solo escalón | 1 |
| 5 | Cuándo ayuda más | Fabiana | 0 de 43 falsas promesas; solo 1 de 48 parcelas buenas descartada | 1 |
| 6 | Cuándo no fiarse | Jc | Sin medidas, sitios nuevos y la confusión entre good y best | 1 |

### App

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 7 | La app | Jc | Demo en vivo: elegir el sitio, rellenar las medidas, pulsar Predecir | 4 |

### Código: datos y validación

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 8 | Cómo se construyó | Jc | Cambio de parte: de lo que hace el modelo a cómo está hecho | 0,5 |
| 9 | Estructura del código | Jc | Siete notebooks, `comun.py`, `final.ipynb` y la app con sus tests | 1,5 |
| 10 | EDA: dos gráficos | Manon | Sin medidas, siempre none; más vigor, mejor clase | 1,5 |
| 11 | Del EDA a las decisiones | Manon | Cada hallazgo llevó a una decisión (ADR-0001 y ADR-0002) | 1,5 |
| 12 | Limpieza | Manon | 46 parcelas sin medidas, un diámetro imposible, siete columnas repetidas | 1,5 |
| 13 | Variables | Manon | Qué entra a cada modelo y qué queda fuera, y por qué | 1,5 |
| 14 | Validación | Manon | Split 70/15/15, validación cruzada, validación por sitio y el gap menor de 5 | 1,5 |

### Código: modelos

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 15 | Los cuatro modelos | Elena | Hiperparámetros elegidos; importancia nativa frente a por permutación | 1,5 |
| 16 | Qué probó cada uno | Elena | Resumen de los cuatro y relevo a cada autor | 1 |
| 17 | Regresión logística | Fabiana | Su modelo: qué probó, qué aprendió y por qué no cumple el gap (6,5) | 2 |
| 18 | Árbol de decisión | Jc | Su modelo: el árbol que memorizaba frente al elegido, 14 veces más pequeño | 2 |
| 19 | SVM lineal | Elena | Su modelo, el ganador: por qué C = 0,045 y no C = 0,07 | 2 |
| 20 | KNN | Manon | Su modelo: gap de 5,4 aceptado y explicado, no forzado | 2 |

### Código: resultado final

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 21 | Comparación en validación | Elena | Solo el SVM y el árbol cumplen el gap; el SVM tiene el mejor F1 | 1,5 |
| 22 | Elección del ganador | Elena | Regla escrita antes de ver los resultados; gana el SVM | 1,5 |
| 23 | Evaluación en test | Elena | F1 0,655, accuracy 0,685 y gap −1,1; el test se abrió una sola vez | 1,5 |
| 24 | Errores e interpretación | Jc | Errores entre clases vecinas; el vigor es la variable que más pesa | 1,5 |
| 25 | Siguientes pasos | Fabiana | Cierre para negocio y para el código | 1 |

## Relevos

**Fabiana 1–5 → Jc 6–9 → Manon 10–14 → Elena 15–16 → Fabiana 17 → Jc 18 → Elena 19 → Manon 20 → Elena 21–23 → Jc 24 → Fabiana 25**

- **De la 16 a la 20 hay cinco cambios seguidos.** En la diapositiva 16 cada autor puede decir una frase de su modelo y pasar a la 17: así el relevo ya está dicho.
- Quien deja la palabra **anuncia a quien viene** («ahora Jc cuenta el árbol») y nadie repite lo que ya se dijo.
- En las preguntas contesta **quien más sabe del tema:** datos y validación, Manon; la app, Jc; el ganador y el test, Elena; los límites del modelo lineal, Fabiana.

## Antes de presentar

- La app tiene que estar **ejecutándose en el equipo desde el que se presenta** (`streamlit run app/main.py`); el enlace de la diapositiva 7 abre `localhost:8501`.
- Rellenar las diapositivas 17 a 20 con su explicación y sus capturas.
- Ensayar los relevos de las diapositivas 15 a 25, donde se alterna entre personas.
- La tecla **N** muestra las notas del orador de cada diapositiva.
- Cada persona puede apoyarse en la explicación de su modelo (carpeta [`modelos/`](modelos/)) para las preguntas.

## Si hay que acortar

- **Con 30 minutos:** quitar la diapositiva 8 (cambio de parte), acortar la demo a 3 minutos y dejar 1 minuto por modelo en las 17 a 20.
- **Con 20 minutos:** pasar rápido por la 12 (limpieza) y la 13 (variables), que están en el informe técnico, y no leer la tabla de la 15.
- Las notas del orador de cada diapositiva dicen qué es lo esencial.

## Cambios posibles

Si alguien prefiere otra parte, lo más sencillo es intercambiar bloques contiguos de tamaño parecido: por ejemplo, Manon puede contar la 9 (estructura del código) y Jc la 12 (limpieza), porque Jc también trabajó en el EDA. Lo que conviene mantener es que cada persona cuente su propio modelo en las diapositivas 17 a 20.

Los tiempos son una estimación para ensayar; se ajustan tras la primera prueba en voz alta.
