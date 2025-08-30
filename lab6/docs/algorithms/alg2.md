# Segundo Modelo: **DistilBERT + CNN** (en PyTorch)

Usar **representaciones contextuales** (DistilBERT) y ponerles encima una **capa convolucional** que "cace" patrones tipo *n-gramas* pero ya embebidos con contexto. Resultado: un clasificador que entiende mejor matices y frases hechas que el baseline léxico.

## 1. Flujo de trabajo — de CSV a predicción

1. **Entrada (CSV crudo)**
   Igual que el baseline:

   - `text` *(string)*: tweet.
   - `target` *(0/1)*: etiqueta real (solo para entrenar/validar).

2. **Preprocesamiento**
   Reutilizamos la **misma limpieza** del baseline (minúsculas, quitar URLs, menciones, hashtags, emojis, puntuación, normalización unicode, compactar espacios, stopwords opcional, conservar números relevantes como "911").
   *Motivo:* aunque BERT puede tragar texto "sucio", esta limpieza reduce ruido y acelera.

3. **Tokenización (HuggingFace)**

   - Modelo: **`distilbert-base-uncased`** -> WordPiece *uncased*.
   - Longitud: **`max_len=128`** (truncamos y *paddeamos*).
   - Generamos **`input_ids`** y **`attention_mask`**.
   - Loteo con *DataLoader* (batch **32**) y *samplers* estratificados (split 80/20).

4. **Representación (backbone)**

   - Pasamos los tokens por **DistilBERT (congelado)** -> tensor `[batch, seq_len, hidden]` (hidden≈768).
   - No ajustamos los pesos del backbone ( `trainable_bert=False` ) para mantener tiempos razonables en CPU.

5. **Cabeza CNN (clasificador)**

   - **Conv1D** con **kernel=3** y **32 filtros** sobre la secuencia contextual (detecta patrones tipo *bigrama/trigrama* ya "entendidos" por BERT).
   - **Global Max Pooling** (se queda con la activación más fuerte por filtro -> "el patrón ocurrió").
   - **Dropout=0.5** para regularizar.
   - **Capa densa** con **sigmoide** -> probabilidad de "desastre".

6. **Entrenamiento**

   - Optimizador con **`lr=1e-3`**; *early stopping* por **`val_loss`** con **paciencia=2**.
   - Épocas objetivo: **10**; si el *val\_loss* deja de mejorar, se corta antes (ocurrió en tu corrida).

7. **Evaluación y selección**

   - Métricas: **Accuracy**, **Precision**, **Recall**, **F1**, **matriz de confusión**.
   - En la ejecución (CPU), se observó:

     - **F1 ≈ 0.773**, **ACC ≈ 0.821** (mejor que la línea base).
     - **CM**: tn=785, fp=84, fn=189, tp=465.
   - Se guardan **tokenizer** y **modelo** en `./models/bert_cnn/{tokenizer, model}`.

8. **Inferencia**

   - Entrada: un **tweet crudo**.
   - Proceso: tokenización -> DistilBERT (freeze) -> CNN -> probabilidad.
   - Salida por tweet: **probabilidad** y **etiqueta** con umbral **0.5** (ajustable).
   - Uso operativo: **cargar artefactos guardados** y predecir (sin re-entrenar).

## 2. ¿Qué aprende este modelo que el baseline no?

- **Contexto**: "fire" en "**forest** fire" no es lo mismo que "this mixtape is **fire**". DistilBERT desambigua por contexto.
- **Patrones locales**: la **CNN** es un *cazador de frases* sobre embeddings contextuales:
  `suicide bomber`, `oil spill`, `heat wave`, `train derailment`… señales muy discriminativas.
- **Robustez a variantes**: WordPiece maneja errores y palabras raras (`califor##nia`, `wild##fire`), lo que ayuda en textos cortos y ruidosos.

## 3. Entradas y salidas (I/O)

### Entrenamiento

- **Input**: DataFrame (`text`, `target`) ya limpiado; hiperparámetros (max\_len, batch, lr, paciencia, etc.).
- **Output**:

  - Modelo guardado: `./models/bert_cnn/model`
  - Tokenizer: `./models/bert_cnn/tokenizer`
  - Métricas (F1/ACC/CM) y logs de entrenamiento.

### Inferencia

- **Input**: tweet en texto plano + **umbral** (p. ej., 0.5).
- **Output**:

  - **Probabilidad** de desastre.
  - **Etiqueta** binaria (según umbral).
- **Operación**: se usan directamente los artefactos guardados (tokenizer+modelo); latencia razonable incluso en CPU.

## 4. Decisiones de diseño (y trade-offs)

- **Congelar DistilBERT**: acelera mucho en CPU y reduce overfitting con dataset mediano; con GPU podríamos *descongelar* para ganar más (especialmente últimas capas).
- **`max_len=128`**: equilibrio entre cubrir la mayoría de tweets y no disparar costo.
- **CNN con kernel=3**: "bigrama/trigrama" efectivo; se podría añadir un bloque multi-kernel (3/4/5) si se busca exprimir más.
- **Early stopping (paciencia=2)**: evita sobreentrenar la cabeza CNN cuando la validación se estanca.
- **Umbral**: 0.5 por defecto; si te importa más *recall* (no perder desastres), bájalo un poco (p. ej., 0.45).

## 5. Resultados y lectura rápida

- En los logs: **mejoró** frente al baseline (F1 0.773 vs 0.768; ACC 0.821 vs 0.804).
- **Perfil de errores**: bajaron **FP** respecto a la base y subieron algo los **FN** (tn=785, fp=84, fn=189, tp=465). Si deseas menor FN, baja el umbral o permite *fine-tuning* parcial del backbone.

## 6. Ventajas y limitaciones

**Ventajas:**

- Captura **semántica contextual** y **frases clave** con la CNN.
- Mejor **generalización** ante sinónimos, paráfrasis y ruido de redes.
- Mejor F1/ACC que la línea base en la corrida reportada.

**Limitaciones:**

- En **CPU** es más lento de entrenar que el baseline; inferencia sigue siendo aceptable.
- **Sarcasmo/ironía** y referencias culturales siguen siendo difíciles.
- Congelar el backbone limita el techo de performance; con GPU, *fine-tuning* puede subir unos puntos.
