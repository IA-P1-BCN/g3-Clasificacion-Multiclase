# AGENTS.md

## Objetivo
Equipo de 4 personas que resuelve el ejercicio del bootcamp `docs/business/EXERCISE_SPECS.md` (nivel **Esencial**) con el dataset **Eucalyptus** (OpenML 188, objetivo `Utility`, 5 clases).
Referencias: la guía sugerida `docs/workshop_clasificacion/WORKSHOP.md` (con sus notebooks de ejemplo) y la guía de proceso `docs/machine_learning/guia_proyecto_ml.md`.
Las reglas de ML comunes (datos, evaluación, contrato de modelos, app) están en `docs/acuerdos.md`: léelas antes de tocar un notebook o la app.

## Acuerdos
- Notebooks, en orden de merge: `00_general` (problema, limpieza común y split), `01_eda`, `02_regresion_logistica`, `03_arbol_decision`, `04_svm`, `05_knn`, `06_conclusiones`.
- Una persona por algoritmo; `06_conclusiones` lo hacemos entre todos.
- `nbmerge` los junta en `final.ipynb`.
- La app (Streamlit) vive en `app/` y sus tests en `tests/`.

## Agent skills

### Issue tracker
GitHub Issues en un Projects board: milestones = épicas, issues = historias, sub-issues = tareas técnicas. Ver `docs/agents/issue-tracker.md`.

### Domain docs
Single-context: `GLOSSARY.md` + `docs/adr/` en la raíz. Ver `docs/agents/domain.md`.

## Reglas generales
- Divulgación progresiva: aquí lo esencial y el detalle en `docs/`.
- Flujo: rama `feat/…`, `fix/…`, `docs/…` (conventional branches) → PR directa a `main` (protegida, al menos 1 review). No hay rama `dev`.
- Conventional commits, con la descripción en español.
- TDD solo en la app (`app/` + `tests/` con pytest). Los notebooks no llevan tests.
- Todo lo que se escribe en el proyecto va en español (notebooks, docs, commits, textos de la app).
- Entorno mixto Windows/macOS: rutas relativas o `pathlib`, `encoding="utf-8"` explícito, finales de línea LF. Entorno virtual en `.venv/` con `pip install -r requirements.txt`.

## Lo que el agente no debe hacer
- Escribir credenciales en ningún fichero.
- Activar flujos en producción.
- Dejar instrucciones obsoletas: si cambias comandos, rutas o acuerdos, actualiza este fichero.
- Inflar este fichero: el detalle va en `docs/`.
