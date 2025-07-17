# TO-DO: Primera Entrega

## **1. Carga y limpieza de datos**

* [ ] Descargar los archivos de:

  * Precios: hasta 11 julio 2025
  * Importaciones: hasta 2024 y 2025
  * Consumo: hasta 2024 y 2025
* [ ] Unir archivos de cada tipo de datos (importación, consumo, precios)
* [ ] Filtrar únicamente: gasolina super, gasolina regular, diésel (dieselLS desde 2018) y gas licuado
* [ ] Asegurar consistencia en fechas y unidades

## **2. Análisis exploratorio (EDA)**

* [ ] Graficar comportamiento general por tipo de combustible
* [ ] Detectar patrones: picos anuales, estacionalidad, comportamiento en pandemia (2020–2021), últimas tendencias
* [ ] Identificar meses de mayores importaciones y consumos
* [ ] Verificar normalidad (histograma, QQ-plot, test de Shapiro si aplica)
* [ ] Guardar visualizaciones y hallazgos para el reporte

## **3. Selección de 2–3 series de tiempo**

* [ ] Escoger 3 series (mínimo una de precios)

  * Ej: precios gasolina regular, importación diesel, consumo gas licuado
* [ ] Para cada serie:

  * [ ] Definir: fecha inicio, fin y frecuencia
  * [ ] Graficar la serie
  * [ ] Descomponer en tendencia, estacionalidad y residuo
  * [ ] Evaluar estacionariedad (media y varianza)

    * [ ] Gráfico de autocorrelación
    * [ ] Prueba Dickey-Fuller
    * [ ] Aplicar transformaciones o diferenciación si es necesario
* [ ] Anotar observaciones y explicaciones para cada análisis

## **4. Documentación para entrega parcial**

* [ ] Crear documento PDF:

  * Introducción + descripción breve del dataset
  * Análisis exploratorio
  * Análisis detallado de 2 series seleccionadas
* [ ] Subir scripts de Python o R usados
* [ ] Incluir link de Google Drive y del repositorio
