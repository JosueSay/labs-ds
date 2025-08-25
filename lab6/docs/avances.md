# Reporte

El objeivo del proyecto es **clasificar si un tweet se refiere a un desastre real (1) o no (0)**.

## Descripción de los datos

- **id**: Identificador único del tweet.
- **keyword**: Palabra clave asociada al tweet (puede estar en blanco).
- **location**: Ubicación desde donde se envió el tweet (puede estar vacía).
- **text**: El contenido del tweet.
- **target**: Etiqueta binaria (1 = tweet sobre un desastre real, 0 = no relacionado con desastre).

```csv
1,,,Our Deeds are the Reason of this #earthquake May ALLAH Forgive us all,1
235,airplane%20accident,India,OMG Horrible Accident Man Died in Wings of Airplane. <http://t.co/xDxDPrcPnS,1>
```

## Preprocesamiento

### 1. Tokenización y normalización

#### 1.1 Tokenización

**Definición técnica.** Proceso de segmentar una secuencia en **tokens** (palabras, símbolos o subpalabras).  

**Ejemplo.** “El gato saltó la valla.” -> \[`El`, `gato`, `saltó`, `la`, `valla`, `.`].  

**Entrada / salida.**

- **Entrada:** cadena de texto crudo (tweet).
- **Salida:** lista ordenada de tokens.

> **Nota:** En tweets, los **emojis** y artefactos como URLs, menciones `@usuario` y hashtags `#Tema` requieren reglas específicas. Esto es la primera transformación canónica del pipeline.

#### 1.2 Normalización mínima recomendable

- **Minúsculas**, eliminación de **URLs**, **signos de puntuación** no informativos y **espacios extra**.
- Manejo de **stopwords** (artículos, preposiciones) según experimento.
- Los números *informativos* de dejaron (p. ej., “911”).
- Lematización/stemming si mejora la estabilidad del vocabulario.  
Esta etapa aparece como práctica estándar en los materiales de referencia.

### 2. n-gramas: unigramas y bigramas

#### 2.1 Unigramas

**Definición técnica.** Un **unigrama** es un n-grama con $n=1$: cada token individual.  

**Cálculo.** Se cuentan las ocurrencias de cada token en el corpus o subconjuntos (clase 0 vs. 1).  

**Fórmula (frecuencia absoluta).**

$$
\mathrm{tf}(w,d) = \#\text{veces que } w \text{ aparece en el documento } d
$$

**Entrada / salida.**

- **Entrada:** lista de tokens por documento (tweet).
- **Salida:** vector disperso de frecuencias por vocabulario (nivel documento) o tabla de frecuencias (nivel corpus).

**Utilidad.** Capturan señal léxica directa (p. ej., *earthquake*, *fire*). Son la base del conteo de palabras revisado en los apuntes (frecuencias con unigramas/bigramas/trigramas).

#### 2.2 Bigramas

**Definición técnica.** Un **bigrama** es un n-grama con $n=2$: pares de tokens adyacentes, p. ej., `forest fire`.  

**Cálculo.** Deslizar una ventana de tamaño 2 sobre la secuencia tokenizada; contar ocurrencias.  

**Entrada / salida.**

- **Entrada:** lista de tokens por documento.
- **Salida:** vector disperso o tabla de frecuencias de pares (token$*t$, token$*{t+1}$).

**Utilidad.** Aportan **contexto local** (desambiguación: `brush fire` vs. `camp fire`) y suelen mejorar la clasificación de textos cortos.

> **Nota:** Usaremos bigramas si los falsos positivos provienen de palabras ambiguas, los bigramas ayudan a fijar **colocaciones**; en textos muy cortos.

### 3. Representaciones vectoriales

#### 3.1 TF, IDF y TF-IDF

**Definiciones.**

- **TF** (term frequency) en el documento $d$: $\mathrm{tf}(w,d)$ (o una versión normalizada).
- **IDF** (inverse document frequency) en el corpus $D$ con $|D|$ documentos:

$$
\mathrm{idf}(w) = \log\frac{|D|}{1 + |\{d \in D : w \in d\}|}
$$

- **TF-IDF:** pondera términos frecuentes en el documento pero **raros** en el corpus:

$$
\mathrm{tfidf}(w,d) = \mathrm{tf}(w,d)\cdot \mathrm{idf}(w)
$$

**Entrada / salida.**

- **Entrada:** colección de documentos tokenizados; configuración de n-gramas.
- **Salida:** matriz documento-término dispersa (dimensión $|D|\times|V|$).

> **Notas:** TF-IDF sobre **unigramas+bigramas** balancea señal y ruido en tweets; los materiales comparan TF-IDF con embeddings y discuten sus límites ante variantes ortográficas y contexto.

#### 3.2 n-gramas de caracteres

**Definición.** n-gramas construidos a nivel **carácter** (p. ej., $n=3$ a $5$).

**Ventaja.** Robustez ante **faltas**, hashtags pegados y variantes (e.g., `#earthquake!` -> `ear`, `art`, `rth`…).  

**Entrada / salida.**

- **Entrada:** texto crudo o normalizado.
- **Salida:** vector TF-IDF de n-gramas de caracteres.

> **Nota:** Convendrá aplicarlo en dominios con mucho ruido como Twitter y presencia de emojis/ASCII, un fenómeno discutido en los apuntes.

#### 3.3 Embeddings

**Definición.** Mapas densos $\mathbb{R}^n$ que codifican **vecindad semántica**; se entrenan por co-ocurrencia (p. ej., **Word2Vec Skip-Gram** maximiza $p(w_\psi\mid w)$).  

**Formulación (Skip-Gram, esquema).**

$$
\arg\max_{\beta}\prod_{w\in X}\ \prod_{w_\psi\in\Psi(w)} p(w_\psi\mid w;\beta),\quad
p(w_\psi\mid w;\beta) = \frac{e^{v_{w_\psi}\cdot v_w}}{\sum_{w' } e^{v_{w' }\cdot v_w}}
$$

donde $v_w$ y $v_{w_\psi}$ son vectores de palabras.

**Entrada / salida.**

- **Entrada:** corpus tokenizado; ventana de contexto; dimensión $n$.
- **Salida:** diccionario palabra->vector denso.

> **Nota:** Los embeddings manejan bien variantes y contexto, especialmente útiles para NER y señales situacionales en desastres.

## Modelo preliminar de clasificación: Regresión Logística con regularización L2

### 1. Regresión Logística (binaria)

**Definición técnica.** Modelo discriminativo que estima

$$
P(y=1\mid \mathbf{x})=\sigma(\mathbf{w}^\top\mathbf{x}+b),\quad
\sigma(z)=\frac{1}{1+e^{-z}}
$$

donde $\mathbf{x}$ es el vector de características (p. ej., TF-IDF), $\mathbf{w}$ los pesos y $b$ el sesgo.

**Función de pérdida (entropía cruzada).**

$$
\mathcal{L}*{\text{CE}}(\mathbf{w},b)=
-\frac{1}{N}\sum*{i=1}^N\Big[y_i\log \hat{y}_i + (1-y_i)\log (1-\hat{y}_i)\Big]
$$

con $\hat{y}_i=\sigma(\mathbf{w}^\top \mathbf{x}_i+b)$.

**Entrada / salida.**

- **Entrada:** matriz TF-IDF (uni/bi-gramas; opcional n-gramas de caracteres), etiquetas $\{0,1\}$.
- **Salida:** probabilidades $[0,1]$ y etiqueta predicha (umbral típico 0.5).

**Justificación:** Es interpretable (pesos por término) y rápido para textos cortos; se usa como línea base antes de pasar a redes profundas, tal como se reporta en la literatura comparativa de clasificación de tweets de desastres.

### 2. Regularización L2 (Ridge)

Es la penalización sobre la **norma Euclidiana** de los pesos que controla la complejidad del modelo.

**Norma L2.** $\lVert \mathbf{w}\rVert_2=\sqrt{\sum_j w_j^2}$.  

**Pérdida regularizada.**

$$
\mathcal{L}(\mathbf{w},b)=\mathcal{L}_{\text{CE}}(\mathbf{w},b)+\lambda\lVert \mathbf{w}\rVert_2^2
$$

donde $\lambda>0$ es el hiperparámetro de regularización.

**Por qué es relevante.**  

- Reduce **sobreajuste** en espacios de alta dimensión (TF-IDF).  
- Favorece pesos más **pequeños** y soluciones **estables** ante colinealidad de n-gramas.

**Entrada / salida.**

- **Entrada:** como 4.1 + $\lambda$.
- **Salida:** modelo con pesos suavizados; mejor **generalización**.

### 3. Parámetros clave e hiperparámetros

- **Rango de n-gramas:** $(1,2)$ (uni+bi) como punto de partida; ampliar si mejora validación.
- **Vocabulario / corte de frecuencia:** filtrar términos ultra raros (ruido).  
- **Regularización L2 $\lambda$:** seleccionar por validación (o $C=1/\lambda$).  
- **Balanceo de clases:** ponderar si hay desbalance.  
- **Umbral de decisión:** calibrar según **F1**/recall de la clase 1 (desastre).

### 4. Entradas y salidas del pipeline (resumen)

**Entradas generales.**

- Tweets crudos (`text`), opcionalmente `keyword` y `location`.
- Configuración de preprocesamiento (minúsculas, eliminación de URLs, etc.).

**Salidas intermedias.**

- Secuencias de tokens (tokenización).
- Vectores TF-IDF de **unigramas/bigramas** (y/o n-gramas de caracteres).
- Embeddings para análisis comparativo o extracción de rasgos.

**Salidas finales.**

- **Probabilidad** $P(\text{desastre}=1\mid \mathbf{x})$ y **etiqueta** $\{0,1\}$.
- **Importancias** (coeficientes) por término para interpretación del modelo lineal.

### 5. Ventajas y limitaciones (síntesis)

**Ventajas (pipeline TF-IDF + Logística L2).**

- Entrenamiento **rápido** y **estable**; **interpretabilidad** por pesos.
- Captura de **señal léxica** con uni/bi-gramas en textos cortos.

**Limitaciones.**

- No modela **dependencias largas** ni ambigüedad semántica; sensible a ironía/sarcasmo, retos conocidos en redes sociales.

**Relación con métodos avanzados.** La literatura reciente sobre tweets de desastres reporta mejoras al pasar a **CNN + embeddings BERT** (optimización adaptativa como **RMSProp**), por su capacidad para capturar **contexto** y matices semánticos; estos trabajos comparan contra líneas base clásicas (p. ej., logística, árboles).

### 6. Recomendaciones para el reporte de unigramas y bigramas

1) **Descriptivos básicos.** Top-20 por clase (desastre/no), con frecuencia y, si aplica, **peso TF-IDF**. (Apuntes sugieren contar frecuencias con uni/bi/tri-gramas).
2) **Señal discriminativa.** Mostrar términos y pares con mayor diferencia relativa entre clases.  
3) **Inspección de errores.** Revisar bigramas que corrigen ambigüedad de unigramas (p. ej., `forest fire` vs. `dumpster fire` metafórico).  
4) **Documentar decisiones.** Inclusión/exclusión de hashtags, números clave y emojis (los apuntes señalan su complejidad y costo token).

### 7. Glosario rápido

- **Unigrama / Bigrama:** token individual / par adyacente; base de conteo y TF-IDF.
- **TF-IDF:** peso que combina frecuencia local y rareza global del término.  
- **Embeddings:** vectores densos que codifican similitud contextual (Word2Vec Skip-Gram).
- **Regresión Logística:** clasificador probabilístico para dos clases con función sigmoide.  
- **L2 (regularización):** penalización por la **norma Euclidiana** de los pesos para evitar sobreajuste.
