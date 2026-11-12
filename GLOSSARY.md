# Conservación del suelo con eucalipto

Vocabulario del problema: predecir lo útil que es una parcela de ensayo de eucalipto para conservar el suelo, en las colinas de la Isla Norte de Nueva Zelanda.

## Language

**Parcela**:
Una unidad de ensayo donde se plantó un lote de eucaliptos; es una fila del dataset.
_Avoid_: muestra, árbol, registro

**Sitio**:
El lugar donde está la parcela (columna `Abbrev`); varias parcelas comparten sitio, clima y año.
_Avoid_: localidad, zona, ubicación

**Clase de utilidad**:
Lo útil que es la parcela para conservar el suelo, en cinco niveles ordenados: none, low, average, good y best. Es el objetivo que se predice.
_Avoid_: utility, etiqueta, categoría, calidad

**Parcela sin medidas**:
Una parcela sin ninguna medida de supervivencia, vigor, resistencia a insectos ni forma; en los datos siempre es de clase none.
_Avoid_: parcela vacía, nulos, parcela muerta

**Vigor**:
La puntuación del crecimiento del árbol en la parcela (columna `Vig`); es la medida que más se parece a la clase de utilidad.
_Avoid_: salud, fuerza

**Modelo ganador**:
El modelo con mayor F1 macro en validación entre los que no sobreajustan; es el único que se evalúa en test y el que usa la app.
_Avoid_: mejor modelo, modelo final, modelo elegido
