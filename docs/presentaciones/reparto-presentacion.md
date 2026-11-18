# Reparto de la presentación entre cuatro personas

Propuesta para la presentación completa ([`presentacion-eucalyptus.html`](presentacion-eucalyptus.html), 25 diapositivas, más la 18 bis): **20 minutos como máximo**, unos **5 minutos por persona** (el profesor pide unos 4, con margen según el número de personas), participación equilibrada y demo de la app.

**Regla del reparto:** cada persona cuenta un bloque seguido de diapositivas. Solo se alterna entre personas en las diapositivas 17 a 20, donde cada una presenta su propio modelo.

El reparto sigue quién hizo cada parte según el historial del repositorio; se puede cambiar de común acuerdo.

## Resumen

| Persona | Diapositivas | Qué cuenta | Tiempo | Apoyo para las preguntas |
|---|---|---|---|---|
| **Fabiana** (regresión logística) | 1 a 6 y 17 | Historia de negocio: problema, solución, resultado y límites; después, su modelo | 5 min | [`modelos/regresion-logistica.html`](modelos/regresion-logistica.html) |
| **Jc** (app, árbol de decisión) | 7 a 9, 18 y 18 bis | Demo de la app y estructura del código; después, su modelo | 5 min | [`modelos/arbol-decision.html`](modelos/arbol-decision.html) |
| **Manon** (EDA y KNN) | 10 a 16 y 20 | De los datos a la validación y presentación de los cuatro modelos; después, su modelo | 5 min | [`modelos/knn.html`](modelos/knn.html) |
| **Elena** (SVM e informe técnico) | 19 y 21 a 25 | Su modelo (el ganador); después, comparación, ganador, test, errores y siguientes pasos | 5 min | [`modelos/svm.html`](modelos/svm.html) |

## Por qué así

- **Cuatro bloques seguidos, más los cuatro modelos:** el único vaivén entre personas es el de las diapositivas 17 a 20.
- **Fabiana abre** con la historia de negocio, que no necesita jerga.
- **Jc lleva la demo** porque construyó la app y sus tests, y la estructura del código.
- **Manon lleva los datos** (EDA, limpieza, variables y validación) y presenta los cuatro modelos (15 y 16), que dan paso al relevo.
- **Elena cierra:** el SVM es el ganador y ella redactó el informe técnico, así que cuenta la comparación, el test y los siguientes pasos.

## Orden de intervención

### Idea de negocio (≈ 6,25 min)

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 1 | Portada | Fabiana | Qué se va a contar y en qué orden: negocio, app y código | 0,5 |
| 2 | El problema | Fabiana | 736 parcelas en 16 sitios; calificación de none a best | 0,75 |
| 3 | La solución | Fabiana | El modelo repite la calificación a partir de las medidas. No se prueba si el eucalipto mejora el suelo | 0,75 |
| 4 | El resultado | Fabiana | Acierta unas 7 de cada 10 parcelas; 34 de los 35 errores son de un solo escalón | 0,75 |
| 5 | Cuándo ayuda más | Fabiana | 0 de 43 falsas promesas; solo 1 de 48 parcelas buenas descartada | 0,5 |
| 6 | Cuándo no fiarse | Fabiana | Sin medidas, sitios nuevos y la confusión entre good y best | 0,5 |
| 7 | La app | Jc | Demo en vivo con cuatro casos, cada uno con su concepto: parcela de validación (pipeline completo, paso 10), sin medidas → none por regla (ADR-0001, fuga de datos), valor imposible (validación de la entrada) y sitio nuevo (ADR-0002) | 2,5 |

### Parte técnica: datos y validación (≈ 7 min)

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 8 | Cómo se construyó | Jc | Cambio de parte: de lo que hace el modelo a cómo está hecho | 0,25 |
| 9 | Estructura del código | Jc | Por qué `comun.py` (mismas reglas para comparar los cuatro modelos), `final.ipynb` y la app con 32 tests hechos con TDD (Nivel Avanzado) | 0,75 |
| 10 | EDA: dos gráficos | Manon | Sin medidas, siempre none; más vigor, mejor clase | 0,75 |
| 11 | Del EDA a las decisiones | Manon | Cada hallazgo llevó a una decisión (ADR-0001 y ADR-0002) | 0,5 |
| 12 | Limpieza | Manon | 46 parcelas sin medidas, un diámetro imposible, siete columnas repetidas | 0,5 |
| 13 | Variables | Manon | Qué entra a cada modelo y qué queda fuera | 0,5 |
| 14 | Validación | Manon | Split 70/15/15, validación cruzada, validación por sitio y el gap menor de 5 | 0,75 |
| 15 | Los cuatro modelos | Manon | Hiperparámetros elegidos; importancia nativa frente a por permutación | 0,5 |
| 16 | Qué probó cada uno | Manon | Resumen de los cuatro y relevo a cada autor | 0,25 |

### Los cuatro modelos (≈ 5,25 min)

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 17 | Regresión logística | Fabiana | Su modelo: qué probó, qué aprendió y por qué no cumple el gap (6,5) | 1,25 |
| 18 | Árbol de decisión | Jc | Su modelo en 3 pasos: sin límites memoriza (gap 46); la regla del gap deja competir solo las 42 combinaciones que no memorizan y gana un árbol de 10 hojas en vez de 139 con el mismo F1 en CV; funciona con parcelas nuevas (0,562) y se entiende (vigor, 72 % de la importancia) | 0,75 |
| 18 bis | El código del árbol | Jc | Pipeline (sin fuga de datos), rejilla de 120 combinaciones y `refit` con nuestra regla del gap en lugar del mayor F1 a ciegas | 0,75 |
| 19 | SVM lineal | Elena | Su modelo, el ganador: por qué C = 0,045 y no C = 0,07 | 1,25 |
| 20 | KNN | Manon | Su modelo: gap de 5,4 aceptado y explicado, no forzado | 1,25 |

### Resultado final y cierre (≈ 3,75 min)

| Nº | Diapositiva | Quién | Qué hay que dejar claro | Min |
|---|---|---|---|---|
| 21 | Comparación en validación | Elena | Solo el SVM y el árbol cumplen el gap; el SVM tiene el mejor F1 | 0,75 |
| 22 | Elección del ganador | Elena | Regla escrita antes de ver los resultados; gana el SVM | 0,75 |
| 23 | Evaluación en test | Elena | F1 0,655, accuracy 0,685 y gap −1,1; el test se abrió una sola vez | 1 |
| 24 | Errores e interpretación | Elena | Errores entre clases vecinas; el vigor es la variable que más pesa | 0,75 |
| 25 | Siguientes pasos | Elena | Cierre para negocio y para el código | 0,5 |

## Relevos

**Fabiana 1–6 → Jc 7–9 → Manon 10–16 → Fabiana 17 → Jc 18 y 18 bis → Elena 19 → Manon 20 → Elena 21–25**

- Solo hay vaivén en las diapositivas 17 a 20, y hasta ahí lo orienta la 16: Manon cierra el resumen de los cuatro modelos y cada autor continúa con el suyo.
- Quien deja la palabra **anuncia a quien viene** («ahora Jc cuenta el árbol») y nadie repite lo que ya se dijo.
- **Preguntas:** no responde una sola persona. Contesta **quien más sabe del tema** (negocio y límites del modelo lineal, Fabiana; app y estructura del código, Jc; datos y validación, Manon; ganador, test y errores, Elena) y, en lo de cada modelo, su autor.

## Antes de presentar

- La app tiene que estar **ejecutándose en el equipo desde el que se presenta** (`streamlit run app/main.py`); el enlace de la diapositiva 7 abre `localhost:8501`.
- Rellenar las diapositivas 17 a 20 con su explicación y sus capturas.
- Ensayar con **cronómetro**: el límite de 20 minutos es estricto, y 25 diapositivas obligan a pasar rápido por las de datos (10 a 14).
- La tecla **N** muestra las notas del orador de cada diapositiva.
- El pie de cada diapositiva dice **quién la presenta** (por ejemplo, «Jc · 7»). Una diapositiva extra no mueve la numeración: lleva `data-bis` en su `<section>` y sale como «18 bis». Si cambia el reparto, se actualiza `PONENTES` en `construir_presentacion.py`.
- La presentación publicada está en https://ia-p1-bcn.github.io/g3-Clasificacion-Multiclase/ (GitHub Pages, solo la presentación). Se actualiza sola al mergear en `main` cambios en `presentacion-eucalyptus.html` (workflow `publicar-presentacion`; también se puede lanzar a mano desde la pestaña *Actions*).
- Cada persona puede apoyarse en la explicación de su modelo (carpeta [`modelos/`](modelos/)) para las preguntas.

## Si hay que acortar

- Pasar la 8 (cambio de parte), la 12 y la 13 a una sola frase.
- Reducir la demo a 2 minutos.
- Las notas del orador de cada diapositiva dicen qué es lo esencial.

## Cambios posibles

Se pueden intercambiar bloques contiguos de tamaño parecido; por ejemplo, Manon puede contar la 9 (estructura del código) y Jc la 12 (limpieza), porque Jc también trabajó en el EDA. Lo que conviene mantener es que cada persona cuente un bloque seguido y su propio modelo en las diapositivas 17 a 20.

Los tiempos son una estimación para ensayar; se ajustan tras la primera prueba en voz alta.
