# Lab7

En`data` existen dos conjuntos de **5,000 tweets** recopilados de las cuentas de **@traficogt** y **@BArevalodeLeon**, con datos recolectados hasta el **12 de septiembre de 2024**.  

El objetivo es seleccionar uno de los dos conjuntos de datos y aplicar las técnicas de limpieza, preprocesamiento, análisis de redes sociales y análisis de contenido para responder las preguntas planteadas.  

- **@traficogt**: Tweets relacionados con el tráfico vehicular en la ciudad de Guatemala.  
- **@BArevalodeLeon**: Tweets relacionados con el presidente de Guatemala, Bernardo Arévalo.  

## Problemas de Investigación

### Problema 1: @traficogt

- ¿Cómo complicó la época de lluvia el tráfico en toda la ciudad?  
- ¿Cuáles son las áreas de la ciudad que más se congestionaron?  
- ¿Se mantendrán esas áreas como puntos de congestión este año?  
- Según los usuarios, ¿en qué horarios ocurren los mayores atascos?  

### Problema 2: @BArevalodeLeon

- ¿Qué aceptación tenía Bernardo Arévalo como presidente de Guatemala durante el año?  
- ¿Cuál es su nivel de popularidad en la actualidad?  

## Rúbrica de Evaluación del Proyecto

### 1. Limpieza y Preprocesamiento (12 puntos)

- **5 puntos**: Describe detalladamente todas las actividades de limpieza y preprocesamiento, incluyendo normalización de nombres de usuario y menciones.  
- **4 puntos**: Identifica y extrae menciones, respuestas y retweets de cada tweet para análisis de red.  
- **3 puntos**: Crea una estructura de datos (DataFrame, matriz de adyacencia) que represente interacciones como grafos dirigidos (nodos = usuarios, aristas = retweets, menciones, respuestas).  

### 2. Análisis Exploratorio (20 puntos)

- **5 puntos**: Análisis del número de tweets, usuarios únicos, menciones y hashtags frecuentes. Generación de nube de palabras.  
- **5 puntos**: Realización de análisis adicionales que ayuden a entender mejor los datos.  
- **10 puntos**: Preguntas e insights:  
  - **6 puntos**: Formular al menos 3 preguntas interesantes surgidas del análisis exploratorio.  
  - **4 puntos**: Responder estas preguntas con base en los datos.  

### 3. Análisis de la Topología de la Red (15 puntos)

- **5 puntos**: Crear y visualizar grafos dirigidos, destacando nodos más conectados y relaciones de poder en las comunidades.  
- **5 puntos**: Explicar claramente las relaciones encontradas.  
- **3 puntos**: Calcular densidad, diámetro y coeficiente de agrupamiento.  
- **2 puntos**: Discutir la relevancia de estas métricas en el contexto de la red.  

### 4. Identificación y Análisis de Comunidades (15 puntos)

- **4 puntos**: Aplicar un algoritmo adecuado (ej. Louvain) para detectar comunidades.  
- **3 puntos**: Explicar la elección del algoritmo y su aplicación.  
- **5 puntos**: Graficar todas las comunidades, resaltando las más grandes e influyentes, además de un gráfico específico para las 3 comunidades más grandes.  
- **3 puntos**: Caracterizar las 3 comunidades más grandes (tamaño, interacciones, temas principales).  

### 5. Análisis de Influencers y Nodos Clave (10 puntos)

- **4 puntos**: Calcular y explicar centralidad de grado, intermediación y cercanía.  
- **6 puntos**: Identificar y justificar quiénes son los usuarios más influyentes según estas métricas.  

### 6. Detección y Análisis de Grupos Aislados (8 puntos)

- **4 puntos**: Calcular y explicar métricas de centralidad (grado, intermediación, cercanía).  
- **4 puntos**: Identificar subredes o grupos aislados y analizar su dinámica e influencia en la red principal.  

### 7. Análisis de Contenido y Sentimiento (10 puntos)

- **5 puntos**: Realizar un análisis de tópicos para identificar temas principales en los tweets, explicando su relación con las comunidades detectadas.  
- **5 puntos**: Realizar análisis de sentimiento con técnicas NLP, identificando la polaridad (positiva, negativa, neutral) y explicando resultados.  

### 8. Interpretación y Contexto (20 puntos)

- **6 puntos**: Explicar cómo los influencers y comunidades influyen en la formación de opinión pública, contextualizando los hallazgos en un marco social más amplio.  
- **6 puntos**: Responder las preguntas planteadas en la sección de problemas a resolver.  
- **8 puntos**: Redactar conclusiones que resuman los hallazgos del análisis de la red social con el conjunto de datos seleccionado.  

## Librerías Recomendadas para el Proyecto en Python

### 1. Análisis de la Topología de la Red

- **networkx**: Biblioteca principal para construir, manipular y analizar redes. Permite calcular métricas de centralidad, cohesión y detectar comunidades.  
- **igraph (Python)**: Optimizada para análisis rápidos y escalables en redes grandes.  
- **pygraphviz**: Orientada a la visualización de grafos complejos.

### 2. Análisis de Influencers y Nodos Clave

- **networkx**: Incluye funciones para calcular métricas de centralidad (grado, intermediación, cercanía, etc.), útiles para identificar usuarios influyentes en la red.

### 3. Análisis de Contenido y Sentimiento

- **nltk**: Herramientas para procesamiento de lenguaje natural, tokenización, análisis de frecuencia y extracción de características de texto.  
- **TextBlob**: API simple para análisis de sentimiento y corrección gramatical.  
- **VADER (nltk.sentiment)**: Especializado en análisis de sentimiento en redes sociales, con alta precisión en textos cortos como tweets.  
- **spaCy**: Motor de NLP avanzado y rápido, ideal para análisis profundos como detección de entidades nombradas (NER).  
- **transformers (Hugging Face)**: Biblioteca de modelos de última generación (ej. BERT) para análisis de sentimientos y clasificación de texto.

### 4. Visualización Avanzada

- **plotly**: Gráficos interactivos para exploración dinámica de datos.  
- **PyVis**: Visualización interactiva de redes.  
- **Bokeh**: Alternativa a plotly para dashboards y gráficos interactivos.  
- **Gephi**: Herramienta externa que permite importar datos desde networkx o igraph para visualización avanzada.  
- **igraph**: Soporta visualizaciones estáticas de comunidades y grafos.

## Flujo de Trabajo

### 1. Descarga de Datos

- Descargar los archivos: `traficogt.txt`, `tioberny.txt`.

### 2. Carga de Datos

- Cargar los archivos en o **Python**.

### 3. Limpieza y Preprocesamiento

- Convertir texto a mayúsculas o minúsculas.
- Eliminar caracteres especiales (#, @, apóstrofes).
- Eliminar URLs.
- Identificar y decidir si eliminar emoticones.
- Quitar signos de puntuación.
- Eliminar artículos, preposiciones y conjunciones (stopwords).
- Eliminar números si interfieren con el análisis.
- Extraer metadatos de los tweets (ID, texto, menciones, retweets, favoritos).
- Eliminar duplicados.
- Normalizar nombres de usuario y menciones.
- Crear una estructura de datos eficiente (DataFrame o matriz de adyacencia).
- Representar interacciones como grafos dirigidos (nodos = usuarios, aristas = interacciones).

### 4. Análisis Exploratorio

- Identificar menciones, respuestas y retweets.
- Calcular estadísticas básicas (número de tweets, usuarios únicos, hashtags frecuentes).
- Generar nube de palabras.
- Formular y responder al menos 3 preguntas derivadas de la exploración.

### 5. Análisis de la Topología de la Red

- Construcción y visualización de grafos dirigidos.
- Identificación de nodos más conectados y relaciones de poder.
- Cálculo de métricas clave:
  - Densidad.
  - Diámetro.
  - Coeficiente de agrupamiento.

### 6. Detección y Análisis de Comunidades

- Aplicar algoritmos de detección de comunidades.
- Visualizar y caracterizar comunidades (tamaño, interacciones, temas).
- Graficar las 3 comunidades más grandes.

### 7. Análisis de Influencers y Nodos Clave

- Identificación de usuarios influyentes con métricas de centralidad:
  - Grado.
  - Intermediación.
  - Cercanía.

### 8. Detección de Grupos Aislados

- Identificar subredes y nodos aislados.
- Analizar su dinámica y relevancia como nichos dentro de la red.

### 9. Análisis de Contenido y Sentimiento

- Realizar análisis de sentimiento (positivo, negativo, neutral).
- Identificar temas principales mediante análisis de tópicos.
- Comparar temas entre redes de `@traficogt` y `@bernardoarevalodeleon`.

### 10. Interpretación y Contexto

- Explicar hallazgos en un marco más amplio.
- Analizar la influencia de comunidades e influencers en la opinión pública.

Aquí tienes la separación actualizada considerando que **solo se trabajará con el dataset de `@traficogt`**:

## Repartición de tareas

### Sección 1 – Descarga y Carga de Datos

**Persona A:**

- Descargar `traficogt.txt`.
- Cargar el archivo en Python y verificar integridad.

### Sección 2 – Limpieza y Preprocesamiento

**Persona A:**

- Normalización de texto (minúsculas, eliminación de caracteres especiales, URLs, stopwords, etc.).
- Extracción de metadatos de cada tweet.
- Eliminación de duplicados.
- Normalización de nombres de usuario y menciones.
- Construcción de DataFrame inicial.

### Sección 3 – Análisis Exploratorio

**Persona A:**

- Estadísticas básicas: número de tweets, usuarios únicos, hashtags frecuentes.
- Nube de palabras.
- Formular 3 preguntas derivadas de la exploración y responderlas.

### Sección 4 – Construcción y Análisis de Redes (Topología)

**Persona B:**

- Identificación de menciones, respuestas y retweets.
- Construcción de grafos dirigidos (nodos = usuarios, aristas = interacciones).
- Cálculo de densidad, diámetro y coeficiente de agrupamiento.
- Visualización de grafos y explicación de relaciones.

### Sección 5 – Detección y Análisis de Comunidades

**Persona B:**

- Aplicar algoritmo Louvain (u otro adecuado).
- Visualización de todas las comunidades.
- Caracterización de las 3 más grandes (tamaño, interacciones, temas principales).

### Sección 6 – Influencers y Nodos Clave

**Persona B:**

- Cálculo de centralidades (grado, intermediación, cercanía).
- Identificación y justificación de los usuarios más influyentes.

### Sección 7 – Grupos Aislados

**Persona B:**

- Identificación de subredes y nodos aislados.
- Análisis de su dinámica e influencia.

### Sección 8 – Análisis de Contenido y Sentimiento

**Persona A:**

- Análisis de sentimiento con TextBlob/VADER.
- Análisis de tópicos (temas principales en los tweets).

### Sección 9 – Interpretación y Contexto

- **Persona A:** Relacionar hallazgos de contenido/sentimiento con las preguntas de investigación de `@traficogt` (impacto de la lluvia, áreas más congestionadas, horarios, persistencia de puntos críticos).
- **Persona B:** Relacionar hallazgos de red/comunidades e influencers con las mismas preguntas de investigación.
- Redacción conjunta de conclusiones generales.

✅ **Distribución final:**

- **Persona A:** Secciones 1, 2, 3, 8, y parte de 9.
- **Persona B:** Secciones 4, 5, 6, 7, y parte de 9.
