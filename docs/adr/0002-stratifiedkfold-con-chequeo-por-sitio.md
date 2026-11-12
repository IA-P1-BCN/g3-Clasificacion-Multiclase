# StratifiedKFold común pese a la fuga por sitio

El sitio marca mucho la clase, así que con StratifiedKFold las parcelas de un mismo sitio caen a la vez en train y en validación, y las métricas sobreestiman cómo rendiría el modelo en un sitio nuevo. Aun así usamos `StratifiedKFold` de 5 folds como esquema común, porque lo pide el enunciado y mantiene las proporciones de cada clase. Lo complementamos con un `StratifiedGroupKFold` agrupado por sitio, que solo se usa en el informe para medir cuánto se infla la métrica.

## Considered Options
- `StratifiedGroupKFold` para todo: métricas más realistas para sitios nuevos, pero más bajas e inestables (hay sitios con 2 y 5 parcelas).
