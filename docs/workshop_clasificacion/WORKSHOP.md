# Workshop: Algoritmos de Clasificación en Machine Learning

## Descripción

Este repositorio contiene material educativo completo sobre algoritmos de clasificación en Machine Learning. El workshop está diseñado para proporcionar tanto la teoría fundamental como ejemplos prácticos implementados en Python, permitiendo a los estudiantes aprender los conceptos clave y aplicarlos en casos de uso reales.

## Objetivos de Aprendizaje

Al completar este workshop, serás capaz de:
- Entender los fundamentos de los algoritmos de clasificación supervisada
- Implementar y evaluar diferentes modelos de clasificación
- Interpretar métricas de evaluación como precisión, recall, F1-score y AUC-ROC
- Aplicar técnicas de preprocesamiento de datos y selección de características
- Comparar el rendimiento de diferentes algoritmos en problemas reales

## Contenido del Repositorio

### Algoritmos de Clasificación

#### 1. **Regresión Logística** - [`ejemplo_regresion_logistica.ipynb`](ejemplo_regresion_logistica.ipynb)
- **Concepto**: Clasificación probabilística usando la función sigmoide
- **Características**:
  - Predice probabilidades entre 0 y 1
  - Fronteras de decisión lineales
  - Interpretable y eficiente
- **Ejemplo Práctico**: Predicción de aprobación de exámenes según horas de estudio
- **Temas Cubiertos**:
  - Función logística/sigmoide
  - Coeficientes e interpretación
  - Curvas de probabilidad

#### 2. **Árboles de Decisión** - [`ejemplo_arbol_decision.ipynb`](ejemplo_arbol_decision.ipynb)
- **Concepto**: Decisiones secuenciales basadas en reglas if-then-else
- **Características**:
  - Altamente interpretable
  - Maneja características categóricas y numéricas
  - Propenso al overfitting
- **Ejemplo Práctico**: Decisión de adopción de mascotas
- **Temas Cubiertos**:
  - Criterios de división (Gini, Entropía)
  - Visualización del árbol
  - Importancia de características

#### 3. **Support Vector Machines (SVM)** - [`ejemplo_SVM.ipynb`](ejemplo_SVM.ipynb)
- **Concepto**: Maximización del margen entre clases
- **Características**:
  - Encuentra hiperplanos óptimos de separación
  - Robusto ante outliers
  - Soporte para kernels no lineales
- **Ejemplo Práctico**: Clasificación de tipos de flores
- **Temas Cubiertos**:
  - Vectores de soporte
  - Márgenes y fronteras de decisión
  - Kernels lineales y polinómicos

#### 4. **K-Nearest Neighbors (KNN)** - [`ejemplo_knn.ipynb`](ejemplo_knn.ipynb)
- **Concepto**: Clasificación basada en proximidad a vecinos más cercanos
- **Características**:
  - Algoritmo basado en instancias (no paramétrico)
  - Clasificación por votación mayoritaria de k vecinos
  - Sensible a la escala de las características
- **Ejemplo Práctico**: Clasificación de tipos de frutas basada en peso y tamaño
- **Temas Cubiertos**:
  - Distancia Euclidiana
  - Selección del valor óptimo de k
  - Visualización de fronteras de decisión

### Evaluación de Modelos - [`ejemplo_evaluacion_algoritmos_clasificacion.ipynb`](ejemplo_evaluacion_algoritmos_clasificacion.ipynb)

**Métricas de Evaluación Fundamentales**:
- **Matriz de Confusión**: Visualización de aciertos y errores
- **Precisión (Precision)**: TP / (TP + FP)
- **Sensibilidad (Recall)**: TP / (TP + FN) 
- **F1-Score**: Media armónica de precisión y recall
- **Curva ROC y AUC**: Evaluación de capacidad discriminativa

**Ejemplo Práctico**: Clasificación de clientes bancarios para predicción de depósitos

### Proyecto Integrador - [`Pokemon_Legendary.ipynb`](Pokemon_Legendary.ipynb)

**Desafío Completo**: Clasificación de Pokémon Legendarios
- **Dataset**: 801 Pokémon con 41 características
- **Objetivo**: Predecir si un Pokémon es legendario basándose en sus estadísticas
- **Proceso Completo**:
  - Análisis Exploratorio de Datos (EDA)
  - Limpieza y preprocesamiento
  - Ingeniería de características
  - Comparación de múltiples algoritmos
  - Optimización de hiperparámetros
  - Evaluación y selección del mejor modelo

## Tecnologías Utilizadas

### Librerías Principales
```python
import pandas as pd              # Manipulación de datos
import numpy as np               # Operaciones numéricas
import matplotlib.pyplot as plt  # Visualización
import seaborn as sns           # Visualización estadística

# Scikit-Learn
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, roc_curve, roc_auc_score
```

### Entorno Recomendado
- Python 3.8+
- Jupyter Notebook o JupyterLab
- Anaconda/Miniconda (recomendado)

## Prerrequisitos

### Conocimientos
- Fundamentos de Python
- Conceptos básicos de estadística
- Álgebra lineal básica
- Familiaridad con Pandas y NumPy (deseable)

### Configuración del Entorno
```bash
# Crear entorno virtual
conda create -n ml_classification python=3.9
conda activate ml_classification

# Instalar dependencias
pip install pandas numpy matplotlib seaborn scikit-learn jupyter

# Instalar dependencias adicionales para el proyecto Pokémon
pip install missingno
```

## Cómo Usar Este Repositorio

### 1. **Aprendizaje Secuencial** (Recomendado)
```
- Regresión Logística - Rama 1
- Árboles de Decisión - Rama 2
- Support Vector Machine (SVM) - Rama 3
- K-Nearest Neighbors (KNN) - Rama 4
- Métricas de evaluación - Rama 5
```

### 2. **Aprendizaje por Algoritmo**
- Selecciona el algoritmo de tu interés
- Cada notebook es autocontenido con teoría y práctica

### 3. **Proyecto Práctico**
- Ve directamente a `Pokemon_Legendary.ipynb` para un desafío completo
- Incluye todo el pipeline de ML desde EDA hasta evaluación

## Estructura de Cada Notebook

### Formato Consistente
1. **Banner y Título**: Identificación clara del tema
2. **Introducción Teórica**: Conceptos fundamentales explicados de forma clara
3. **Explicación Matemática**: Fórmulas y algoritmos detallados
4. **Ejemplo Práctico**: Implementación paso a paso con datos reales
5. **Interpretación de Resultados**: Análisis y conclusiones
6. **Ejercicios Adicionales**: Oportunidades de práctica

### Metodología de Enseñanza
- **Aprender Haciendo**: Cada concepto se acompaña de código ejecutable
- **Visualizaciones**: Gráficos para entender conceptos abstractos
- **Ejemplos del Mundo Real**: Casos de uso prácticos y relevantes

## Casos de Uso Ejemplificados

### 1. **Clasificación de Frutas** (KNN)
- **Problema**: Identificar manzanas vs naranjas por peso y tamaño
- **Aprendizaje**: Distancias, vecindario, visualización de decisiones

### 2. **Predicción de Aprobación de Exámenes** (Regresión Logística)
- **Problema**: ¿Aprobará un estudiante según horas de estudio?
- **Aprendizaje**: Probabilidades, curvas sigmoideas, interpretación

### 3. **Clasificación de Flores** (SVM)
- **Problema**: Distinguir especies por características de pétalos
- **Aprendizaje**: Márgenes, vectores de soporte, kernels

### 4. **Adopción de Mascotas** (Árboles de Decisión)
- **Problema**: ¿Adoptará una familia una mascota?
- **Aprendizaje**: Reglas de decisión, interpretabilidad

### 5. **Clientes Bancarios** (Evaluación)
- **Problema**: Predecir depositors bancarios
- **Aprendizaje**: Métricas de evaluación, comparación de modelos

### 6. **Pokémon Legendarios** (Proyecto Integrador)
- **Problema**: Clasificar Pokémon legendarios vs normales
- **Aprendizaje**: Pipeline completo de ML, EDA, feature engineering

## Resultados de Aprendizaje Esperados

### Habilidades Técnicas
- Implementar algoritmos de clasificación desde cero
- Evaluar modelos usando métricas apropiadas
- Interpretar resultados y tomar decisiones basadas en datos
- Comparar el rendimiento de diferentes algoritmos
- Optimizar hiperparámetros para mejorar el rendimiento

### Habilidades Conceptuales
- Entender cuándo usar cada algoritmo
- Identificar sesgos y limitaciones de los modelos
- Comunicar resultados de forma clara y efectiva
- Diseñar experimentos de machine learning

## Conceptos Clave Cubiertos

### Fundamentos de Clasificación
- Aprendizaje supervisado vs no supervisado
- Conjuntos de entrenamiento, validación y prueba
- Overfitting y underfitting
- Selección de características

### Preprocesamiento de Datos
- Limpieza de datos y manejo de valores faltantes
- Normalización y estandarización
- Codificación de variables categóricas
- Análisis exploratorio de datos (EDA)

### Optimización de Modelos
- Validación cruzada
- Búsqueda en cuadrícula (GridSearch)
- Selección de hiperparámetros
- Curvas de aprendizaje

## Progresión Sugerida de Dificultad

### **Nivel Principiante**
- `ejemplo_knn.ipynb`
- `ejemplo_regresion_logistica.ipynb`

### **Nivel Intermedio**
- `ejemplo_SVM.ipynb`
- `ejemplo_arbol_decision.ipynb`
- `ejemplo_evaluacion_algoritmos_clasificacion.ipynb`

### **Nivel Avanzado**
- `Pokemon_Legendary.ipynb` (Proyecto completo)

## Recursos Adicionales

### Documentación Oficial
- [Scikit-Learn](https://scikit-learn.org/stable/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)

### Datasets Adicionales para Práctica
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Scikit-learn Built-in Datasets](https://scikit-learn.org/stable/datasets.html)
