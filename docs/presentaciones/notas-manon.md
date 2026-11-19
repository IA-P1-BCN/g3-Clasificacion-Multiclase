# Notas de Manon para la presentación

Mis diapositivas son la 10 a la 16 (≈ 5 minutos). Entro después de Jc (diapositiva 9) y paso a Elena en la 17.

| Diap. | Título | Min |
|---|---|---|
| 10 | Dos gráficos que cambiaron el diseño | 1 |
| 11 | De cada hallazgo, una decisión | 0,75 |
| 12 | Limpieza | 0,75 |
| 13 | Variables | 0,5 |
| 14 | Validación | 1 |
| 15 | Los cuatro modelos | 0,5 |
| 16 | Qué probó cada uno | 0,5 |

## 10 · Dos gráficos que cambiaron el diseño (1 min)

- Empiezo con el EDA: dos gráficos cambiaron cómo construimos todo.
- **Sin medidas, siempre `none`:** las 46 parcelas sin ninguna medida (sitios Mor y Wen) son las 46 `none`. Entre las 469 con medidas, `none` es solo el 17 %.
- Si el modelo aprendiera «sin medidas significa `none`», parecería mejor de lo que será con datos nuevos que sí traigan medidas. Eso es **fuga de información**.
- **Más vigor, mejor clase:** de las 191 parcelas con vigor mayor que 3, 165 son `good` o `best`; de las 104 con vigor 2 o menos, ninguna.
- Es una asociación, no una causa.

## 11 · De cada hallazgo, una decisión (0,75 min)

- Cada hallazgo llevó a una decisión; leo la tabla de arriba abajo, sin detenerme.
- **ADR-0001:** las parcelas sin medidas salen solo de train; en validación, test y app se predice `none` por regla.
- **ADR-0002:** `StratifiedKFold` como validación común y, aparte, `StratifiedGroupKFold` por sitio, solo para medir cuánto se infla la métrica.
- **F1 macro** como métrica: good es el 29 % y best el 14 %, el desequilibrio es moderado y F1 macro trata igual las cinco clases.

## 12 · Limpieza (0,75 min)

- Qué había que arreglar: 46 parcelas sin medidas, un diámetro imposible, 22 supervivencias ausentes, 7 columnas que repiten el sitio.
- **El código:** esta es la función `limpiar` de `comun.py`, la que llama `01_eda`. Quita las columnas del sitio, pone a hueco el diámetro erróneo y, en train, quita las parcelas sin medidas.
- **El gráfico:** un diámetro de 42 085 cm, un árbol de 420 m. Tras la limpieza el máximo es de 53,9 cm.
- Se limpia una sola vez, tras el split 70/15/15, y los cuatro notebooks leen los mismos CSV.
- De 736 parcelas: 515 en train, 110 en validación y 111 en test; en train quedan 469 al quitar las 46 sin medidas.

## 13 · Variables (0,5 min)

- La tabla dice qué entra a cada modelo; cada persona definió el preprocesado del suyo.
- Fuera en todos: `Rep` y `PMCno`, que son identificadores y un modelo podría memorizarlos. La especie tiene 25 valores, muchos con 2 o 3 parcelas, y en SVM y KNN solo añadía sobreajuste.
- La mediana, porque no la arrastran los valores extremos.
- **El código de la derecha** es el preprocesado del KNN: mediana y escala para las numéricas, one-hot para el sitio.
- **El bloque de abajo** es común a los cuatro: las listas de `comun.py`.
- Variables nuevas: ninguna, el EDA no mostró una combinación clara.

## 14 · Validación (1 min)

- Split 70/15/15, estratificado.
- Misma vara para todos: la misma validación cruzada de 5 folds y la comprobación por sitio.
- **Gap = F1 de train menos F1 de validación con medidas, menor de 5 puntos.**
- Las parcelas sin medidas de validación y test no pasan por el modelo: se predice `none` antes de calcular, y se dan las métricas sobre todo el conjunto y solo con medidas.
- El test se abre **una sola vez**, en `06_conclusiones`, con el ganador.

## 15 · Los cuatro modelos (0,5 min)

- Cuatro algoritmos, una persona por algoritmo; la tabla tiene los hiperparámetros elegidos.
- La importancia de variables es **nativa** en la logística y el árbol, y **por permutación** en SVM y KNN.
- El C tan bajo del SVM (mucha regularización) lo protege del sobreajuste. El KNN no regulariza: guarda los datos.

## 16 · Qué probó cada uno (0,5 min)

- Una frase por modelo; cada etiqueta lleva el F1 de validación y el gap, y el límite es 5.
- **Regresión logística** (0,468 · gap 6,5): peso de clases y regularización fuerte; separa mal las clases intermedias y su gap la descarta.
- **Árbol** (0,562 · gap 3,6): el de mejor nota memorizaba (gap de 43); el elegido es 14 veces más pequeño.
- **SVM** (0,636 · gap 3,0): C = 0,07 puntuaba más pero memorizaba; con C = 0,045 cumple.
- **KNN** (0,552 · gap 5,4): lo explico en «Si me preguntan».
- **Cierro:** «Solo el árbol y el SVM cumplen el gap; Elena cuenta la comparación y el ganador».

## Si me preguntan

### Sobre mi modelo, el KNN
- **¿Qué hiciste?** k = 41, voto uniforme y distancia Manhattan; imputación por mediana, estandarización y el sitio en one-hot.
- **¿Qué probaste?** Una rejilla de 48 combinaciones con validación cruzada. Con voto por distancia memoriza train (F1 de 1, gap de unos 43). Solo 8 combinaciones cumplen el gap en CV y elegí la de mayor F1. Añadir la especie o quitar dos medidas flojas no mejoró más que el ruido.
- **¿Por qué el gap de 5,4 se acepta?** Pasa el límite por 0,4; en CV era 2,1 y la validación con medidas son 95 parcelas, así que unas pocas respuestas lo mueven. Con pesos por distancia sería de unos 43 puntos: eso sí es memorizar.
- **¿Dónde falla?** Acierta bien `none` y `good`, pero de 16 parcelas `best`, 15 las marca como `good`: con k = 41 ganan los vecinos de la clase más numerosa.
- **¿Qué pesa?** Sobre todo el vigor (0,14) y la supervivencia (0,09).
- F1 de validación 0,552 (0,524 solo con medidas).

### Sobre datos y validación
- **¿Por qué no se usa la especie?** 25 valores con pocas parcelas cada una; en KNN añade 25 columnas dispersas que distorsionan las distancias, y la validación cruzada lo confirmó (F1 de 0,533 a 0,503 con k = 41).
- **¿Por qué quitar las parcelas sin medidas?** Todas son `none`: si entran en train, el modelo aprende un atajo que no valdrá con datos nuevos (ADR-0001).
- **¿Por qué dos validaciones?** La común es al azar; la de por sitio mide cuánto se infla la métrica cuando el sitio ya se ha visto (ADR-0002). En sitios nuevos el KNN baja de 0,533 a 0,492.
- **¿Por qué 736 pasan a 469?** 70/15/15 da 515 en train; se quitan las 46 sin medidas. Validación (110) y test (111) conservan todas y las sin medidas se predicen `none` por regla.
