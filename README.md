# g3 · Clasificación multiclase (Eucalyptus)

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/IA-P1-BCN/g3-Clasificacion-Multiclase/blob/main/final.ipynb)
![Python](https://img.shields.io/badge/python-3.14-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-orange)

> El botón de Colab abre `final.ipynb`, el notebook final con todos los demás en orden. Se genera en la entrega con `python unir_notebooks.py`; hasta entonces el enlace no funciona.

## Qué hacemos
Predecimos la **utilidad** (`Utility`) de un lote de semillas de eucalipto para la conservación del suelo, en 5 clases ordenadas: `none` < `low` < `average` < `good` < `best`. Datos: *Eucalyptus Soil Conservation* ([OpenML 188](https://www.openml.org/d/188)), 736 parcelas de ensayo en Nueva Zelanda.

Es el proyecto grupal de clasificación multiclase de Factoría F5, **Nivel Esencial** ([enunciado](docs/business/EXERCISE_SPECS.md)). Entregables: modelo con overfitting < 5 puntos, app en Streamlit, informe y presentaciones.

## Resultados
Métrica principal: **F1 macro**. Se mide en validación (110 parcelas) y las parcelas sin medidas se predicen con la regla `none`.

| Modelo | F1 validación | Gap (puntos) | Estado |
|---|---|---|---|
| Dummy (referencia) | 0.244 | — | baseline a superar |
| [Regresión logística](02_regresion_logistica.ipynb) | — | — | implementada; pendiente de ejecución completa (#38) |
| Árbol de decisión | 0.562 | 3.6 ✅ | PR #69 |
| SVM | — | — | en curso (PR #68) |
| KNN | — | — | en curso |

El modelo ganador se elige y se evalúa en test en `06_conclusiones`.

La regresión logística incluye el pipeline, la búsqueda de hiperparámetros solo en train, las dos CV, métricas con y sin parcelas sin medidas, coeficientes y análisis de errores. Sus cifras se publicarán después de ejecutar y verificar el notebook completo.

## Notebooks (en orden)
| Notebook | Qué hace | Responsable |
|---|---|---|
| `00_general` | Problema, métrica y split | equipo |
| `01_eda` | EDA, limpieza común y datos en `data/` ([informe](docs/informe-eda.md)) | @ManonChab |
| [`02_regresion_logistica`](02_regresion_logistica.ipynb) | Pipeline, CV, evaluación, interpretación y exportación | @fabileoruf |
| `03_arbol_decision` | Modelo de árbol de decisión | @jcxk |
| `04_svm` | Modelo SVM | @elenaalmansacampos |
| `05_knn` | Modelo KNN | @ManonChab |
| `06_conclusiones` | Comparación, modelo ganador y test | equipo |

## Estructura
```
comun.py            librería común: la usan todos los notebooks
unir_notebooks.py   junta 00 → 06 en final.ipynb (nbmerge)
data/               train, val y test limpios (los genera 01_eda)
models/             pipeline de cada modelo (.joblib)
resultados/         cifras de cada modelo (.json) para 06_conclusiones
docs/               acuerdos, ADRs, enunciado y guías
app/, tests/        app de Streamlit y sus tests (próximamente)
```

## Empezar
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python unir_notebooks.py         # genera final.ipynb con los notebooks que existan
```

Para ejecutar la regresión logística, abre `02_regresion_logistica.ipynb` desde la raíz del repo en Jupyter o VS Code, selecciona el Python de `.venv` y ejecuta todas las celdas en orden. Lee únicamente los CSV compartidos de train y validación; no necesita volver a descargar OpenML. Al terminar genera `models/02_regresion_logistica.joblib` y `resultados/02_regresion_logistica.json`, y comprueba la recarga del pipeline en un proceso Python nuevo. Ambos archivos se incluyen en la entrega una vez verificada la ejecución.

## Reglas comunes (resumen)
- **`comun.py` es obligatoria:** carga, limpieza, baseline, validación, evaluación y conclusión salen de ahí (`from comun import ...`).
- **Validación:** `StratifiedKFold` de 5 folds y, aparte, una comprobación por sitio ([ADR-0002](docs/adr/0002-stratifiedkfold-con-chequeo-por-sitio.md)).
- **Parcelas sin medidas:** fuera del entrenamiento; en validación, test y la app se predicen `none` por regla ([ADR-0001](docs/adr/0001-excluir-parcelas-sin-medidas.md)).
- **Overfitting:** gap = F1 train − F1 validación con medidas, con signo, menor de 5 puntos.
- **Modelo ganador:** el de mayor F1 macro en toda la validación entre los que cumplen el gap. El test se usa una sola vez, en `06_conclusiones`.

Detalle en [docs/acuerdos.md](docs/acuerdos.md); vocabulario en [GLOSSARY.md](GLOSSARY.md); contexto del reto en [docs/project-brief.md](docs/project-brief.md).

## Cómo trabajamos
- Ramas `feat/…`, `fix/…`, `docs/…` → PR a `main` (protegida, al menos 1 review).
- Conventional commits, en español.
- Historias y subtareas en el [Project](https://github.com/orgs/IA-P1-BCN/projects/60), milestone *Nivel Esencial* ([cómo se escriben](docs/agents/issue-tracker.md)).
- Instrucciones para agentes de IA: [AGENTS.md](AGENTS.md).
