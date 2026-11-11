# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

Early-stage group bootcamp project (IA School, Data Science P2): multiclass classification. There is no application, model, test suite, or build system yet. Current contents:

- `README.md` and `docs/project-brief.md` are identical: the course brief (in Spanish). It defines delivery levels (Essential → Expert) and the hard constraint **overfitting < 5%** (train vs. validation gap). Deliverables: Streamlit/Gradio/Dash app, technical report, business + technical presentations, Trello link, clean branches/commits on GitHub.
- `EDA.ipynb`: the full exploratory analysis (Spanish, train set only). It loads the OpenML **eucalyptus** dataset (`fetch_openml(data_id=188)`, target `Utility`) instead of the suggested Forest Cover Type dataset (OpenML caches the download), does the stratified split, then Loading, Exploration and a conclusion/hand-off.
- `general.ipynb`: the shared notebook following the guide: problem definition, the split, a summary of the EDA findings with a variable table (linking to `EDA.ipynb`), and empty headed sections for later steps.
- `requirements.txt`: pinned deps (numpy, pandas, scipy, scikit-learn, matplotlib, seaborn, joblib, ipykernel) plus unpinned `kagglehub`.

## Environment

Windows, with a local virtualenv at `.venv/` (gitignored). Setup:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Work is done in Jupyter (`ipykernel` is installed); open the notebooks with the `.venv` kernel.

## Conventions

- **Group project**, so use feature branches and clean commits (the brief grades branch management and commit quality). Check `git log` for the existing commit style before committing.
- **Branch flow:** `main` is the stable branch and `dev` is the integration branch. Create a feature branch from `dev` (e.g. `feat/<topic>`, `fix/<topic>`), and open its PR **into `dev`**, never into `main`. `main` only receives `dev` once the group agrees. Commits use Conventional Commits prefixes (`feat:`, `fix:`, `docs:`, `chore:`…) with Spanish descriptions, since the existing history has no convention.
- **Language: Spanish** for everything written into the project: notebook markdown and comments, docs, reports, app UI strings, commit messages. 

## Workflow guide ("Guía de un proyecto de clasificación en ML")

The group follows this 10-step guide (Drive: https://drive.google.com/file/d/1tkeDPFu6PtNIUo2QwB1pfsNPOH-fQlOu/view). Rules that shape the code:

0. **Define the problem first**: what is predicted, which error costs more, which metric defines "good enough", what simple baseline must be beaten, and whether every feature is available at prediction time (else leakage).
1. **Split BEFORE exploring or preprocessing**: train/val/test (e.g. 70/15/15) or train/test + CV, always `stratify=y`; `GroupKFold` if rows share an individual; split by date if time matters. Never touch test until the final evaluation.
2. **EDA on the train set only**: types, class balance, nulls, duplicates, distributions/outliers, categorical cardinality, per-class plots, correlations/VIF, suspect leakage and useless columns.
3. **Preprocessing**: fit on train only, transform val/test. Use `Pipeline` + `ColumnTransformer`. Scale only for linear/SVM/KNN/NN models, not trees.
4. **Feature engineering/selection**: domain ratios/combinations; drop constants and highly correlated features.
5. **Baseline**: `DummyClassifier` (majority class) + simple logistic regression; a complex model must clearly beat them.
6. **Train/compare** with `StratifiedKFold` (5 folds): logistic regression, tree, Random Forest, XGBoost/LightGBM, SVM/KNN. Imbalance, simplest first: `class_weight="balanced"` → decision threshold → SMOTE/undersampling **only inside each train fold**. Check over/underfitting.
7. **Tuning**: GridSearchCV / RandomizedSearchCV / Optuna, always with CV, never looking at test.
8. **Final evaluation**: once, on test; metrics must match step 0 (accuracy only if balanced; otherwise precision/recall/F1/PR-AUC) plus confusion matrix; check subgroup performance; a big val→test drop means leakage or overfit.
9. **Error analysis & interpretation**: inspect misclassified cases, feature importance/SHAP/coefficients.
10. **Deploy & monitor**: save the **whole pipeline** (preprocessing + model) with `joblib`, not just the model; expose as app/API; watch data drift and performance.

Common mistakes to avoid: preprocessing before the split, accuracy on imbalanced data, SMOTE before CV, using test to make decisions, not defining the costliest error up front.

**Team split of work:** the EDA lives in its own `EDA.ipynb` (train set only) and stops before preprocessing; `general.ipynb` only links its findings and variables. Each team member then does their own preprocessing and trains their own model; the group then compares the models and picks one. So the split (`SEMILLA = 42`, 70/15/15 stratified), CV scheme (`StratifiedKFold`, 5 folds) and metrics (macro F1, accuracy, per-class F1) must stay identical across members, and nobody touches the test set before the final choice. Don't preprocess inside `EDA.ipynb`. The split code is duplicated in both notebooks (same seed): change both together.
