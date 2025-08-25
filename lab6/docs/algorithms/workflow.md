# Flujo completo del proceso de clasificación de texto

Paso a paso, cómo un **tweet** pasa de estar en un archivo CSV crudo a convertirse en una **predicción**:  

**¿Se refiere a un desastre real (1) o no (0)?**

## 1. Entrada de datos (CSV original)

El conjunto de datos contiene varias columnas. Ejemplo de cómo luce un registro en crudo:

| id | keyword   | location   | text                                                                 | target |
|----|-----------|------------|----------------------------------------------------------------------|--------|
| 0  | accident  | California | "Just happened a terrible car crash!!! #breaking"                    | 1      |
| 1  | fire      |            | "Dumpster fire at the party 😂"                                      | 0      |
| 2  | earthquake| Mexico City| "Heard about earthquake in Mexico, stay safe everyone."              | 1      |

## 2. Preprocesamiento

### 2.1 Normalización de texto

- Todo el texto se pasa a **minúsculas**.
- Se eliminan URLs, signos de puntuación, hashtags y emojis.
- Se conservan palabras que pueden ser **informativas** (ejemplo: `911`).

**Ejemplo antes y después:**

Texto original:  

- *"Just happened a terrible car crash!!! #breaking"*  

Texto normalizado:  

- *"just happened a terrible car crash"*

### 2.2 Tokenización

Dividimos el texto en **tokens** (palabras separadas).

Ejemplo:

- *"just happened a terrible car crash"* -> \[`just`, `happened`, `a`, `terrible`, `car`, `crash`]

### 2.3 Eliminación de stopwords

Quitamos palabras sin carga semántica fuerte (ejemplo: artículos y preposiciones).

- Tokens antes: \[`just`, `happened`, `a`, `terrible`, `car`, `crash`]  

- Tokens después: \[`happened`, `terrible`, `car`, `crash`]

### 2.4 lematización

Se transforma cada palabra a su forma base.  

Ejemplo: `happened` -> `happen`.

Resultado final: \[`happen`, `terrible`, `car`, `crash`]

## 3. Construcción de representaciones (unigramas y bigramas)

### 3.1 Unigramas

Un **unigrama** es una sola palabra.  

Ejemplo:  

- *"forest fire spreads quickly"* -> \[`forest`, `fire`, `spreads`, `quickly`]

### 3.2 Bigramas

Un **bigrama** son dos palabras consecutivas.  

Ejemplo:  

- *"forest fire spreads quickly"* -> \[`forest fire`, `fire spreads`, `spreads quickly`]

**Resultado combinado (uni + bi):**  

- \[`forest`, `fire`, `spreads`, `quickly`, `forest fire`, `fire spreads`, `spreads quickly`]

## 4. Asignación de pesos a términos (TF-IDF)

Cada término conservado después del preprocesamiento (es decir, sin stopwords, con lemas normalizados y sin ruido como URLs o emojis) recibe un **peso numérico** que refleja qué tan relevante es dentro de un tweet y en comparación con el resto del corpus.

### 4.1 Frecuencia de término (TF)

La **frecuencia de término** mide cuántas veces aparece una palabra en un documento específico.

**Ejemplo:**  
Tweet: `"car crash crash"`  

- `car` = 1  
- `crash` = 2  

En la matriz de representación, este tweet tendrá un valor proporcionalmente más alto en la columna correspondiente a `crash`.

### 4.2 Frecuencia inversa de documento (IDF)

La **frecuencia inversa de documento** mide qué tan exclusiva es una palabra en el corpus.  

- Palabras que aparecen en **muchos documentos** (ejemplo: `car`) reciben **menos peso**.  
- Palabras que aparecen en **pocos documentos** (ejemplo: `earthquake`, `tsunami`, `crash`) reciben **más peso**.

> Nota: como ya eliminamos **stopwords** en el preprocesamiento (`the`, `a`, `and`), estas palabras no forman parte del vocabulario. Por lo tanto, el IDF se aplica únicamente a términos **con carga semántica útil**.

### 4.3 Cálculo TF-IDF

El peso final de un término $w$ en un documento $d$ se obtiene como:

$$
\text{TF-IDF}(w,d) = TF(w,d) \times IDF(w)
$$

### Ejemplo conceptual

Tweet: `"terrible car crash"`

- `crash`: aparece pocas veces en el corpus -> **peso alto (0.9)**  
- `car`: aparece con más frecuencia -> **peso medio-bajo (0.4)**  
- `terrible`: aparece moderadamente -> **peso intermedio (0.6)**  

**Vector resultante para el tweet:**  
\[`terrible`=0.6, `car`=0.4, `crash`=0.9]

## 5. Normalización y regularización

### 5.1 Normalización

Cada tweet se representa como un **vector numérico**.

Ejemplo:  

- Tweet A -> \[0.6, 0.4, 0.9]  
- Tweet B -> \[0.0, 0.0, 1.2]  

Estos vectores se escalan para que no dependan de la longitud del tweet.

### 5.2 Regularización L2

Durante el entrenamiento, se penalizan pesos muy grandes en el modelo:  

$$
\lambda \cdot \sum_j w_j^2
$$

Esto evita que el modelo dependa de una sola palabra aislada (sobreajuste).

## 6. Método de clasificación

### 6.1 Modelo aplicado

**Regresión logística binaria.**  
El modelo recibe un vector TF-IDF y calcula una **probabilidad** de que el tweet sea sobre un desastre real.

Ejemplo conceptual:  
Vector de entrada: \[`terrible`=0.6, `car`=0.4, `crash`=0.9]  
Modelo aplica pesos:  

- `terrible`: +0.5  
- `car`: +0.2  
- `crash`: +1.0  

Cálculo interno:  

$$
z = (0.6\times0.5) + (0.4\times0.2) + (0.9\times1.0) = 1.24
$$

$$
\sigma(z) = \frac{1}{1+e^{-1.24}} \approx 0.77
$$

Resultado: **0.77 -> se predice "desastre real (1)"**.

## 7. Evaluación del modelo

Para medir la calidad del clasificador se usan métricas:

- **Precisión (Precision):** de los predichos como desastre, ¿cuántos lo eran realmente?  
- **Exhaustividad (Recall):** de los desastres reales, ¿cuántos fueron detectados?  
- **F1-score:** equilibrio entre precisión y recall.  
- **Matriz de confusión:** tabla que compara predicciones vs. realidad.

Ejemplo de matriz simple:

|                 | Predicho 0 | Predicho 1 |
|-----------------|------------|------------|
| Real 0 (no)     | 80         | 20         |
| Real 1 (sí)     | 15         | 85         |

## 8. Salida final del sistema

Cada tweet pasa por este flujo y el modelo entrega:

1. **Probabilidad numérica** (ejemplo: 0.77).
2. **Clasificación binaria** (0 = no desastre, 1 = desastre real).

Ejemplo de resultado:

| id | text                                       | Predicción | Probabilidad |
|----|-------------------------------------------|------------|--------------|
| 0  | "Just happened a terrible car crash!!!"    | 1          | 0.77         |
| 1  | "Dumpster fire at the party 😂"            | 0          | 0.12         |
| 2  | "Heard about earthquake in Mexico..."      | 1          | 0.88         |
