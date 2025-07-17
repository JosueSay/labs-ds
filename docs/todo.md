# TO-DO: Primera Entrega

## 1. Carga, limpieza y preparación de datos

* [ ] Descargar los archivos oficiales en formato `.xlsx`:

  * Precios: hasta 11 julio 2025
  * Importaciones: hasta 2024 y 2025
  * Consumo: hasta 2024 y 2025

* [ ] Convertir cada archivo `.xlsx` a `.csv` para facilitar su lectura en Python o R

* [ ] Unir archivos que pertenecen a un mismo tipo de datos:

  * Importaciones 2024 + 2025
  * Consumos 2024 + 2025
  * Precios 2025 ya incluye todo hasta julio

* [ ] Filtrar **solo las columnas necesarias**:

  * Gasolina regular
  * Diésel → usar una columna unificada como "diésel total"
  * Gas licuado (propano)

* [ ] Para la importación de diésel:

  * Desde enero 2001 a diciembre 2017: usar “diésel alto azufre”
  * Desde enero 2018 en adelante: usar “diésel bajo azufre (dieselLS)”
  * Crear nueva serie: **diésel total = diésel alto azufre (hasta 2017) + dieselLS (desde 2018)**

* [ ] Asegurar consistencia en:

  * Formato de fechas (`aaaa-mm`)
  * Frecuencia mensual en consumo/importación
  * Promediar precios diarios a mensual si es necesario
  * Unidades homogéneas (barriles de 42 galones, quetzales/galón, etc.)

## 2. Análisis exploratorio (EDA)

* [ ] Graficar cada tipo de combustible por fuente (consumo, importación, precios)
* [ ] Identificar:

  * Tendencias generales
  * Meses de mayores valores
  * Comportamiento durante pandemia (2020–2021)
  * Comportamiento desde guerra Rusia–Ucrania (2022–2025)
* [ ] Comparar entre tipos de combustibles
* [ ] Evaluar distribución:

  * Histograma y QQ-plot
  * Test de normalidad (opcional)

## 3. Selección y análisis de series de tiempo

Seleccionar **3 series (una por tipo)**:

* Precio mensual de **gasolina regular** (Ciudad Capital)
* Importación mensual de **diésel total**
* Consumo mensual de **gas licuado**

Para cada serie:

* [ ] Definir:

  * Fecha de inicio y fin
  * Frecuencia: mensual
* [ ] Graficar la serie original
* [ ] Descomponer en:

  * Tendencia
  * Estacionalidad
  * Residuo
* [ ] Evaluar **estacionariedad**:

  * En **media**:

    * Graficar función de autocorrelación (ACF)
    * Aplicar prueba de Dickey-Fuller aumentada (ADF)
    * Aplicar diferenciación si no es estacionaria
  * En **varianza**:

    * Analizar si la varianza crece con el tiempo
    * Aplicar transformaciones (como logaritmo) si es necesario
  * Evaluar **estacionalidad**:

    * Visualmente (descomposición)
    * Confirmar con ACF (picos regulares en rezagos)
* [ ] Anotar observaciones:

  * ¿Es estacionaria en media, varianza?
  * ¿Hay estacionalidad?
  * ¿Se requiere transformación o diferenciación?

## 4. Documentación para entrega parcial

* [ ] Crear documento PDF con:

  * Breve introducción al problema
  * Descripción de los datos
  * Análisis exploratorio
  * Análisis detallado de las 3 series (con visualizaciones y conclusiones)
* [ ] Subir:

  * Script en Python (.py / .ipynb) o R (.r / .rmd)
  * Link de Google Drive con el trabajo colaborativo
  * Link del repositorio usado (GitHub, GitLab, etc.)
