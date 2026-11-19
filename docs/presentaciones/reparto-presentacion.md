# Reparto de la presentación entre cuatro personas

Propuesta para la presentación completa ([`presentacion-eucalyptus.html`](presentacion-eucalyptus.html), 22 diapositivas): **20 minutos como máximo**, unos **5 minutos por persona** (el profesor pide unos 4, con margen según el número de personas), participación equilibrada y demo de la app.

**Regla del reparto:** cada persona cuenta un bloque seguido de diapositivas. No se alterna entre personas.

El reparto sigue quién hizo cada parte según el historial del repositorio; se puede cambiar de común acuerdo.

## Resumen

| Persona | Diapositivas | Qué cuenta | Apoyo para las preguntas |
|---|---|---|---|
| **Fabiana** (regresión logística) | 1 a 6 | Historia de negocio: problema, solución, resultado y límites | [`modelos/regresion-logistica.html`](modelos/regresion-logistica.html) |
| **Jc** (app, árbol de decisión) | 7 a 9 | Demo de la app y estructura del código | [`modelos/arbol-decision.html`](modelos/arbol-decision.html) |
| **Manon** (EDA y KNN) | 10 a 16 | De los datos a la validación y presentación de los cuatro modelos | [`modelos/knn.html`](modelos/knn.html) |
| **Elena** (SVM e informe técnico) | 17 a 22 | Comparación, ganador, test, errores, siguientes pasos y cierre | [`modelos/svm.html`](modelos/svm.html) |

## Orden de intervención

| Nº | Diapositiva | Quién |
|---|---|---|
| 1 | Portada | Fabiana |
| 2 | El problema | Fabiana |
| 3 | La solución | Fabiana |
| 4 | El resultado | Fabiana |
| 5 | Cuándo ayuda más | Fabiana |
| 6 | Cuándo no fiarse | Fabiana |
| 7 | La app (demo) | Jc |
| 8 | Cómo se construyó | Jc |
| 9 | Estructura del código | Jc |
| 10 | EDA: dos gráficos | Manon |
| 11 | Del EDA a las decisiones | Manon |
| 12 | Limpieza | Manon |
| 13 | Variables | Manon |
| 14 | Validación | Manon |
| 15 | Los cuatro modelos | Manon |
| 16 | Qué probó cada uno | Manon |
| 17 | Comparación en validación | Elena |
| 18 | Elección del ganador | Elena |
| 19 | Evaluación en test | Elena |
| 20 | Errores e interpretación | Elena |
| 21 | Siguientes pasos | Elena |
| 22 | Gracias | Elena |

Las diapositivas de cada modelo (regresión logística, árbol con su diapositiva de código, SVM y KNN) se han quitado de la presentación; cada explicación sigue disponible en [`modelos/`](modelos/) para las preguntas.

## Relevos

**Fabiana 1–6 → Jc 7–9 → Manon 10–16 → Elena 17–22**

- Quien deja la palabra **anuncia a quien viene** y nadie repite lo que ya se dijo.
- **Preguntas:** contesta **quien más sabe del tema** (negocio y límites, Fabiana; app y estructura del código, Jc; datos, validación y KNN, Manon; ganador, test, errores y SVM, Elena) y, en lo de cada modelo, su autor.

## Antes de presentar

- La app tiene que estar **ejecutándose en el equipo desde el que se presenta** (`streamlit run app/main.py`); el enlace de la diapositiva 7 abre `localhost:8501`.
- Ensayar con **cronómetro**: el límite de 20 minutos es estricto, y 22 diapositivas obligan a pasar rápido por las de datos (10 a 14).
- La tecla **N** muestra las notas del orador de cada diapositiva.
- El pie de cada diapositiva dice **quién la presenta** (por ejemplo, «Jc · 7»). Una diapositiva extra no mueve la numeración: lleva `data-bis` en su `<section>` y sale como «18 bis». Si cambia el reparto, se actualiza `PONENTES` en `construir_presentacion.py`.
- La presentación publicada está en https://ia-p1-bcn.github.io/g3-Clasificacion-Multiclase/ (GitHub Pages, solo la presentación). Se actualiza sola al mergear en `main` cambios en `presentacion-eucalyptus.html` (workflow `publicar-presentacion`; también se puede lanzar a mano desde la pestaña *Actions*).
- Cada persona puede apoyarse en la explicación de su modelo (carpeta [`modelos/`](modelos/)) para las preguntas.

## Si hay que acortar

- Pasar la 8 (cambio de parte), la 12 y la 13 a una sola frase.
- Reducir la demo a 2 minutos.
- Las notas del orador de cada diapositiva dicen qué es lo esencial.

## Cambios posibles

Se pueden intercambiar bloques contiguos de tamaño parecido. Los tiempos son una estimación para ensayar; se ajustan tras la primera prueba en voz alta.
