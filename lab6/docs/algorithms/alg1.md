# Primer Modelo (línea base): TF-IDF + Clasificador Lineal

Dado un **tweet** en texto libre, decide si habla de un **desastre real (1)** o **no (0)**.

## 1. Flujo de trabajo (workflow) — de CSV a predicción

1. **Entrada (CSV crudo)**
   Columnas mínimas:

   - `text` *(string)*: contenido del tweet.
   - `target` *(0/1)*: etiqueta real (solo para entrenamiento y evaluación).

2. **Preprocesamiento** *(limpieza y normalización)*

   - Minúsculas.
   - Eliminación de **URLs**, **menciones** (`@user`), **hashtags** (`#algo`), **emojis** y **puntuación**.
   - Normalización unicode (arregla rarezas tipo "Â, Ã, …").
   - Opción de **remover stopwords** (artículos, preposiciones, etc.).
   - Compactado de espacios y *trimming*.
   - Nota: decidimos **no borrar "911"** y otros posibles números semánticos.

   **Ejemplo (antes -> después):**
   "*The f\$&@ing floods at LA!! Check http\://… #breaking*"
   -> "*floods la check breaking*"

3. **Representación (features)**

   - **TF-IDF** como vectorización principal.
   - Probamos tres vistas del texto:

     - **Unigramas** de palabras (1-gram).
     - **Uni+bi-gramas** de palabras (1-2).
     - **N-gramas de caracteres (3-5)** ← *la que ganó en validación*.
   - ¿Por qué chars 3-5? capturan variantes ("fire" vs "fires"), errores tipográficos, hashtags pegados, y morfología ligera sin depender del token exacto.

4. **Modelo de clasificación**

   - **Regresión Logística** (binaria) con **regularización L2**.
   - Alternativas evaluadas: Naive Bayes y LinearSVC (con calibración opcional).
   - Seleccionamos el combo con **mejor F1** en el *split* estratificado de validación (80/20).

5. **Evaluación y selección**

   - Métricas: **Accuracy**, **Precision**, **Recall**, **F1** y **matriz de confusión**.
   - Mejor configuración observada en los logs: **TF-IDF de caracteres (3-5) + Logistic Regression**

     - F1 ≈ **0.768**, ACC ≈ **0.804**.
     - CM: tn=732, fp=137, fn=161, tp=493.

6. **Salida / Artefactos**

   - **Modelo guardado** como *pipeline* (vectorizador + clasificador) en:
     `./models/baseline_best.joblib`
   - El *pipeline* incluye todo el preprocesamiento de características necesario para predecir.

## 2. Entradas y salidas

### 2.1 Entrenamiento

- **Input:**

  - DataFrame con columnas `text` y `target`.
  - Configuración de limpieza (parámetros on/off), n-gramas y regularización.
- **Output:**

  - Modelo entrenado (pipeline TF-IDF + clasificador).
  - Métricas y figuras de apoyo (nubes de palabras, histogramas, matriz de confusión).
  - Archivo del modelo: `./models/baseline_best.joblib`.

### 2.2 Predicción (inferencia)

- **Input:**

  - Un **tweet** en crudo (string).
  - Umbral de decisión (por defecto **0.5**).
  - Opción de usar el modelo **guardado** (carga rápida) para evitar re-entrenar.

- **Output (por tweet):**

  - **Etiqueta**: `0` (no desastre) o `1` (desastre).
  - **Probabilidad** (si el clasificador la expone): *p(desastre)*.
  - **Umbral** usado en la decisión.

**Ejemplo conceptual:**
Texto: "*flash flooding downtown, roads closed*" -> prob=0.74 -> **pred=1**.

## 3. ¿Qué señales usa realmente?

- **Unigramas/bigramas** de palabras: léxico directo (`fire`, `evacuate`, `flooding`, `crash`).
- **N-gramas de caracteres (3-5):** robustos a errores y variantes ("burn"/"burnt", "suicid\*", "wildfir", "califor", "hirosh", etc.).
- **Lift** por clase (frecuencias relativas) mostró términos distintivos en "desastre" (`fire`, `disaster`, `storm`, `crash`, `hiroshima`, `bombing`) y en "no desastre" (`like`, `new`, `love`, `lol`, `time`).

**¿Vale la pena bigramas/trigramas?**
Sí, especialmente **bigramas**: capturan contexto clave como `forest fire`, `oil spill`, `heat wave`. Corrigen ambigüedades de palabras sueltas (p. ej., "fire" metafórico vs evento real).

## 4. Decisiones de diseño

- **TF-IDF**: lineal, rápido y estable para textos cortos; evita el sesgo a palabras muy frecuentes.
- **L2 (Ridge)**: controla el sobreajuste en un espacio de miles de n-gramas.
- **Chars 3-5**: mejor F1 en validación (menos *misspellings* y más señal en tweets compactos).
- **Remover emojis/URLs**: emojis tienden a añadir ruido en la línea base; URLs suelen ser poco informativas como texto bruto (aunque pueden usarse como *features* específicas si se codifica su presencia).
- **Conservar números relevantes**: "911", "7.1", "MH370" pueden ser *features* de alto valor.

## 5. Cómo interpretar el modelo

- **Pesos de la logística**: cada término tiene un coeficiente; positivo empuja hacia "desastre", negativo hacia "no".
- Puedes listar los **top términos** por peso absoluto para explicar *"por qué"* una predicción fue positiva/negativa.
- La **matriz de confusión** muestra el perfil de errores: en la corrida reportada, el baseline tiende a **algo más de FP que FN**, señal de mejor *recall* que *precision* para la clase 1.
