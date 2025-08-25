# Proyecto de Clasificación de Tweets sobre Desastres

## 1. Descarga de datos

- [ ] Descargar el archivo **`train.csv`**.

## 2. Carga de datos

- [ ] Cargar los datos en **R** o **Python**, según el entorno de trabajo.

## 3. Limpieza y preprocesamiento

- [ ] Documentar en detalle las actividades de preprocesamiento.  
Tareas sugeridas:
  - [ ] Convertir texto a **mayúsculas** o **minúsculas**.  
  - [ ] Eliminar **caracteres especiales** (`#`, `@`, apóstrofes).  
  - [ ] Eliminar **URLs**.  
  - [ ] Eliminar **emoticones**.  
  - [ ] Quitar **signos de puntuación**.  
  - [ ] Eliminar **stopwords** (artículos, preposiciones y conjunciones).  
  - [ ] Quitar **números** si interfieren en la clasificación.  
    - [ ] Evaluar si conservar números relevantes como `911`.

## 4. Frecuencia de palabras

- [ ] Calcular la frecuencia de palabras en tweets de **desastres** y **no desastres**.  
- [ ] Discutir:
  - [ ] ¿Qué palabras ayudan a mejorar el modelo de clasificación?  
  - [ ] ¿Vale la pena explorar **bigramas** o **trigramas** para el contexto?  

## 5. Análisis exploratorio de datos

- [ ] Identificar la palabra más repetida en cada categoría.  
- [ ] Crear una **nube de palabras** con las más frecuentes.  
- [ ] Generar un **histograma** de las palabras más repetidas.  
- [ ] Analizar palabras que aparecen en **todas las categorías**.  

## 6. Modelos de clasificación

- [ ] Construir varios modelos para clasificar tweets en **desastre** o **no desastre**.  
- [ ] Explicar cómo se abordará el **contexto**.  
- [ ] Probar diferentes algoritmos de clasificación.  

## 7. Función de predicción

- [ ] Crear una función donde el usuario ingrese un tweet y el sistema lo clasifique en **desastre** o **no desastre**.  

## 8. Análisis de sentimiento

- [ ] Determinar palabras **positivas, negativas o neutras**.  
- [ ] Calcular la polaridad de cada tweet (**positivo, negativo, neutral**).  
- [ ] Evaluar si conviene mantener **emoticones** para el análisis.  

## 9. Identificación de tweets extremos

- [ ] Encontrar los **10 tweets más negativos** e indicar su categoría.  
- [ ] Encontrar los **10 tweets más positivos** e indicar su categoría.  
- [ ] Comparar:  
  - [ ] ¿Los tweets de desastres reales son más negativos que los de la otra categoría?  

## 10. Inclusión de la variable “negatividad”

- [ ] Crear una variable que mida la **negatividad** de cada tweet.  
- [ ] Incluirla en el dataset y reentrenar el modelo.  
- [ ] Analizar resultados:
  - [ ] ¿Mejoró el rendimiento del modelo?  
  - [ ] Si es así, ¿en qué medida?
