# Reporte Series de Tiempo

## Integrantes

- Flavio Galán - 22386
- Josué Say - 22801

## Repositorio

- [Enlace a GitHub](https://github.com/JosueSay/labs-ds)
- No se trabajó google docs sino md en el repositorio en la carpeta [docs/reporte](https://github.com/JosueSay/labs-ds/blob/main/docs/reporte.md)

## 1. Introducción

El objetivo de este análisis es modelar y predecir el comportamiento de tres series relacionadas con el mercado de combustibles en Guatemala: consumo mensual de diésel, importaciones de gas licuado de petróleo (GLP) y precios de gasolina regular. Para ello se utilizaron datos mensuales entre los años 2000 y 2025, obtenidos de fuentes nacionales y públicas.

El estudio incluye una exploración del comportamiento histórico de las variables, considerando eventos relevantes como la pandemia por COVID-19 y la guerra entre Rusia y Ucrania, que afectaron la oferta y demanda energética a nivel global. Se eligieron las series por su relevancia económica y su diversidad de comportamiento: consumo estable, importaciones volátiles y precios sensibles a factores externos. El análisis busca identificar patrones, evaluar modelos de predicción y proyectar tendencias futuras.

## 2. Descripción de los datos

Los datos utilizados provienen del portal de acceso a la información pública del Ministerio de Energía y Minas de Guatemala. Las series abarcan el periodo 2000 a 2025, con frecuencia mensual, e incluyen variables de consumo, importación y precios de cuatro tipos de combustible: diésel, gasolina regular, gasolina superior y GLP.

Las unidades están expresadas en barriles para consumo e importación y en quetzales por galón o quetzales por cilindro de 25 lb para los precios. Se estandarizaron nombres, formatos de fecha y valores numéricos para facilitar el análisis.

## 3. Preparación y limpieza de datos

Se desarrolló un proceso automatizado para unificar los archivos originales, seleccionar variables relevantes, renombrar columnas y transformar las fechas al formato datetime.

Se implementó un sistema de caché para evitar reprocesamiento innecesario y se estructuraron archivos intermedios en CSV que pueden ser reutilizados.

La limpieza incluyó control de duplicados, revisión de valores extremos y armonización de unidades. Todo el procedimiento se detalla en el notebook entregado.

## 4. Análisis exploratorio

El análisis exploratorio se enfocó en comprender la evolución y comportamiento general de las variables seleccionadas. Se presentan estadísticas descriptivas (media, mediana, máximos y mínimos) por combustible y tipo de variable (consumo, importación y precios), las cuales permiten identificar diferencias en volumen, dispersión y comportamiento.

Se incluyeron histogramas para observar la distribución de cada serie. Estos muestran que la mayoría de las variables presentan asimetría positiva y no siguen una distribución normal. Destaca el diésel como el más estable y el GLP como el más regulado (especialmente en precios).

Además, se graficaron las series de tiempo tanto en forma combinada como individual por combustible, lo cual evidenció tendencias crecientes, caídas durante la pandemia (2020), repuntes posteriores y posibles patrones estacionales. Las gráficas están colocadas en las secciones correspondientes del reporte.

Finalmente, se utilizaron heatmaps mensuales por año para identificar estacionalidad y comportamiento interanual. Estos muestran, por ejemplo, mayor consumo e importación en la segunda mitad del año para varios combustibles, así como picos de precios en 2022. Las visualizaciones permiten reforzar el contexto histórico de cada serie.

**Tabla 1. Estadísticas descriptivas – Consumo mensual (barriles):**

| Combustible | Promedio (barriles) | Mínimo  | Máximo    | Observaciones clave                                               |
| ----------- | ------------------- | ------- | --------- | ----------------------------------------------------------------- |
| Regular     | 405,017             | 160,742 | 942,394   | Alta dispersión. Consumo se ha más que duplicado desde el mínimo. |
| Superior    | 474,466             | 300,243 | 790,948   | Menor varianza relativa que la regular.                           |
| Diésel      | 880,198             | 507,663 | 1,474,651 | El más consumido con diferencia.                                  |
| GLP         | 322,886             | 167,818 | 600,454   | Menor consumo.                                                    |

**Tabla 2. Estadísticas descriptivas – Importaciones mensuales (barriles):**

| Combustible | Promedio (barriles) | Mínimo  | Máximo    | Observaciones clave                           |
| ----------- | ------------------- | ------- | --------- | --------------------------------------------- |
| Regular     | 419,996             | 81,015  | 1,141,366 | Alta variabilidad.                            |
| Superior    | 494,588             | 170,293 | 1,227,174 | Similar a la regular, pero con mayor volumen. |
| Diésel      | 899,561             | 229,765 | 1,617,427 | Confirma alta dependencia.                    |
| GLP         | 422,204             | 100,562 | 1,077,123 | Muy variable, picos fuertes.                  |

**Tabla 3. Estadísticas descriptivas – Precios mensuales (Q/galón):**

| Combustible | Mediana (Q/galón) | Rango Intercuartílico | Máximo | Observaciones clave                                |
| ----------- | ----------------- | --------------------- | ------ | -------------------------------------------------- |
| Regular     | Q30.78            | Q28.28 – Q33.28       | Q40.50 | Aumentos significativos post-2022.                 |
| Superior    | Q32.19            | Q29.51 – Q34.52       | Q43.24 | Precio más alto, pero sigue patrón de la regular.  |
| Diésel      | Q27.73            | Q25.44 – Q31.30       | Q41.27 | Más volátil. Alta subida en eventos críticos.      |
| GLP (25 lb) | Q20.35            | Q19.50 – Q20.69       | Q24.93 | Más estable, pero con picos.                       |

### Histogramas

El análisis de los histogramas revela que ninguna de las variables (consumo, importación o precios) sigue una distribución normal. En el caso del consumo e importación, se observa una fuerte asimetría positiva, especialmente en gasolina regular y GLP, con presencia de valores extremos que reflejan eventos puntuales de alta demanda. El diésel destaca por ser el más estable y con mayor volumen en ambas dimensiones, lo que lo convierte en un buen candidato para modelado directo. En cuanto a los precios, las gasolinas regular y superior presentan distribuciones más simétricas, mientras que el diésel muestra alta variabilidad, probablemente influenciada por factores externos. El GLP, por su parte, presenta una distribución escalonada, indicando posible regulación o control estatal.

<div style="text-align: center;">
  <img src="../images/histogramas/consumo_histograma.png" alt="Histograma Consumos" height="400"/>
</div>

<div style="text-align: center;">
  <img src="../images/histogramas/importaciones_histograma.png" alt="Histograma Importaciones" height="400"/>
</div>

<div style="text-align: center;">
  <img src="../images/histogramas/precios_histograma.png" alt="Histograma Precios" height="400"/>
</div>

### Series de tiempo

Las series de tiempo de consumo, importaciones y precios reflejan tendencias crecientes sostenidas, interrumpidas por eventos externos como la pandemia en 2020 y choques de precios en 2022. El diésel domina en volumen, mientras que el GLP muestra un crecimiento reciente. Los precios son más volátiles y responden a factores internacionales. Hay indicios de estacionalidad y comportamientos estructurales distintos por tipo de combustible.

**Consumos:**

<div style="text-align: center;">
  <img src="../images/series_tiempo/consumo/consumo_combinada.png" alt="Serie de tiempo para consumos" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/series_tiempo/consumo/consumo_regular.png" alt="Consumo combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/series_tiempo/consumo/consumo_superior.png" alt="Consumo combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/series_tiempo/consumo/consumo_diesel.png" alt="Consumo combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/series_tiempo/consumo/consumo_glp.png" alt="Consumo combustible GLP" height="280"/>
    </td>
  </tr>
</table>

**Importaciones:**

<div style="text-align: center;">
  <img src="../images/series_tiempo/importaciones/importaciones_combinada.png" alt="Serie de tiempo para importaciones" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/series_tiempo/importaciones/importaciones_regular.png" alt="Importación combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/series_tiempo/importaciones/importaciones_superior.png" alt="Importación combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/series_tiempo/importaciones/importaciones_diesel.png" alt="Importación combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/series_tiempo/importaciones/importaciones_glp.png" alt="Importación combustible GLP" height="280"/>
    </td>
  </tr>
</table>

**Precios:**

<div style="text-align: center;">
  <img src="../images/series_tiempo/precios/precios_combinada.png" alt="Serie de tiempo para precios" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/series_tiempo/precios/precios_regular.png" alt="Precio combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/series_tiempo/precios/precios_superior.png" alt="Precio combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/series_tiempo/precios/precios_diesel.png" alt="Precio combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/series_tiempo/precios/precios_glp.png" alt="Precio combustible GLP" height="280"/>
    </td>
  </tr>
</table>

### HeatMap mensual por año

El consumo muestra una tendencia creciente sostenida desde 2015, con caídas en 2020 y picos frecuentes en la segunda mitad del año, especialmente en diésel y gasolina regular. Las importaciones siguen un patrón similar, reforzando la relación entre demanda interna y abastecimiento externo, aunque con mayor variabilidad mensual. En cuanto a precios, se observa un fuerte incremento en 2022 (especialmente en diésel y gasolina) seguido de una estabilización gradual. GLP destaca por su estabilidad tanto en consumo como en precios.

**Consumos:**

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/heatmap/consumo/consumo_regular.png" alt="Consumo combustible regular" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/heatmap/consumo/consumo_superior.png" alt="Consumo combustible superior" height="300"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/heatmap/consumo/consumo_diesel.png" alt="Consumo combustible diésel" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/heatmap/consumo/consumo_glp.png" alt="Consumo combustible GLP" height="300"/>
    </td>
  </tr>
</table>

**Importaciones:**

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/heatmap/importaciones/importaciones_regular.png" alt="Importación combustible regular" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/heatmap/importaciones/importaciones_superior.png" alt="Importación combustible superior" height="300"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/heatmap/importaciones/importaciones_diesel.png" alt="Importación combustible diésel" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/heatmap/importaciones/importaciones_glp.png" alt="Importación combustible GLP" height="300"/>
    </td>
  </tr>
</table>

**Precios:**

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/heatmap/precios/precios_regular.png" alt="Precio combustible regular" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/heatmap/precios/precios_superior.png" alt="Precio combustible superior" height="300"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/heatmap/precios/precios_diesel.png" alt="Precio combustible diésel" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/heatmap/precios/precios_glp.png" alt="Precio combustible GLP" height="300"/>
    </td>
  </tr>
</table>

## 5. Análisis de casos especiales

### Comportamiento en pandemia (2020-2021)

Las importaciones y precios de combustibles en Guatemala reflejaron los efectos inmediatos del confinamiento y la posterior reactivación económica. En importaciones, se observó una fuerte caída entre marzo y mayo de 2020, seguida de una recuperación progresiva, con repuntes más marcados en diésel y superior. El GLP mostró alta volatilidad. En precios, todos los combustibles experimentaron incrementos sostenidos durante 2021, especialmente la gasolina regular y superior, alineados con el alza global del crudo. El GLP, en cambio, mostró aumentos escalonados.En conjunto, las gráficas evidencian una respuesta inicial de choque en volúmenes importados, seguida de una normalización parcial con alzas de precios.

**Consumos:**

<div style="text-align: center;">
  <img src="../images/special_cases/pandemia_2020-2021/consumo/consumo_combinado.png" alt="Serie de tiempo para consumos" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/consumo/consumo_regular.png" alt="Consumo combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/consumo/consumo_superior.png" alt="Consumo combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/consumo/consumo_diesel.png" alt="Consumo combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/consumo/consumo_glp.png" alt="Consumo combustible GLP" height="280"/>
    </td>
  </tr>
</table>

**Importaciones:**

<div style="text-align: center;">
  <img src="../images/special_cases/pandemia_2020-2021/importaciones/importaciones_combinado.png" alt="Serie de tiempo para importaciones" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/importaciones/importaciones_regular.png" alt="Importación combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/importaciones/importaciones_superior.png" alt="Importación combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/importaciones/importaciones_diesel.png" alt="Importación combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/importaciones/importaciones_glp.png" alt="Importación combustible GLP" height="280"/>
    </td>
  </tr>
</table>

**Precios:**

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/precios/precios_regular.png" alt="Precios combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/precios/precios_superior.png" alt="Precios combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/precios/precios_diesel.png" alt="Precios combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/pandemia_2020-2021/precios/precios_glp.png" alt="Precios combustible GLP" height="280"/>
    </td>
  </tr>
</table>

### Comportamiento reciente (2022 - 2025)

Durante el período 2022–2025, Guatemala enfrentó un entorno energético marcado por la volatilidad postpandemia y los efectos indirectos de la guerra en Ucrania. Los precios de los combustibles se dispararon en 2022, alcanzando niveles récord, y aunque comenzaron a descender gradualmente desde 2023, persistieron oscilaciones que reflejan la inestabilidad global. Las importaciones de combustibles se mantuvieron activas, con el diésel liderando el volumen, pero mostrando variabilidad significativa, especialmente en GLP. El consumo interno mostró una recuperación firme luego del impacto del COVID-19, con tendencias estacionales claras y una demanda creciente en todos los productos, particularmente diésel y GLP.

**Consumos:**

<div style="text-align: center;">
  <img src="../images/special_cases/periodo_2022_2025/consumo/consumo_combinado.png" alt="Serie de tiempo para consumos" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/consumo/consumo_regular.png" alt="Consumo combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/consumo/consumo_superior.png" alt="Consumo combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/consumo/consumo_diesel.png" alt="Consumo combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/consumo/consumo_glp.png" alt="Consumo combustible GLP" height="280"/>
    </td>
  </tr>
</table>

**Importaciones:**

<div style="text-align: center;">
  <img src="../images/special_cases/periodo_2022_2025/importaciones/importaciones_combinado.png" alt="Serie de tiempo para importaciones" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/importaciones/importaciones_regular.png" alt="Importación combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/importaciones/importaciones_superior.png" alt="Importación combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/importaciones/importaciones_diesel.png" alt="Importación combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/importaciones/importaciones_glp.png" alt="Importación combustible GLP" height="280"/>
    </td>
  </tr>
</table>

**Precios:**

<div style="text-align: center;">
  <img src="../images/special_cases/periodo_2022_2025/precios/precios_combinado.png" alt="Serie de tiempo para precios" height="500"/>
</div>

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/precios/precios_regular.png" alt="Precios combustible regular" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/precios/precios_superior.png" alt="Precios combustible superior" height="280"/>
    </td>
  </tr>
  <tr>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/precios/precios_diesel.png" alt="Precios combustible diésel" height="280"/>
    </td>
    <td style="border: none;">
      <img src="../images/special_cases/periodo_2022_2025/precios/precios_glp.png" alt="Precios combustible GLP" height="280"/>
    </td>
  </tr>
</table>

## 6. Selección de series para modelado

Se eligieron tres series para el modelado: **precio de gasolina regular**, **consumo de diésel** e **importación de GLP**.

- **Gasolina regular (precio):** es una de las más utilizadas por el parque vehicular liviano y tiene alta sensibilidad social. Fue seleccionada para modelar precios por su relevancia económica y comportamiento volátil en los últimos años, especialmente durante eventos como la pandemia y la guerra en Ucrania.

- **Diésel (consumo):** es el combustible más consumido históricamente en el país, clave para el transporte pesado, comercio y logística. Su análisis permite entender la dinámica productiva y movilidad nacional.

- **GLP (importación):** aunque menos consumido, el GLP es esencial para el uso doméstico. Se eligió esta serie por su crecimiento reciente, alta variabilidad y la posible influencia de subsidios o regulaciones.

## 7. Modelado

### Serie de precios de gasolina regular

#### Inicio, fin y frecuencia de la serie

- **Inicio:** enero 2022
- **Fin:** julio 2025
- **Frecuencia:** diaria

#### Gráfico y observaciones preliminares

- Se observa un pico de precios durante 2022, con una tendencia a la baja en los años siguientes.
- No se aprecia estacionalidad visual evidente, pero sí cierta ciclicidad irregular.
- Los precios del 2021 fueron excluidos por considerarse atípicos.

<div style="text-align: center;">
  <img src="../images/modelado/serie1/inciso_b.png" alt="Serie Temporal de Precios de Combustible Tipo 'regular' (2022–2025)" height="300"/>
</div>

#### Descomposición de la serie

- Se realizó descomposición clásica en componentes: tendencia, estacionalidad y residuo.
- La serie no es estacionaria en media ni en varianza.
- La media y la varianza cambian significativamente a lo largo del tiempo.

<div style="text-align: center;">
  <img src="../images/modelado/serie1/inciso_c.png" alt="Descomposición de la Variable 'regular'" height="300"/>
</div>

#### Transformación de la serie

- Se aplicó una primera diferenciación para intentar estabilizar la media.
- La prueba de Dickey-Fuller sobre la serie diferenciada dio un **p-value ≈ 1.09e-13**, lo cual confirma estacionariedad en media.
- La serie transformada fue utilizada para modelado.

| Métrica                   | Test 1                 | Test 2                 |
|---------------------------|------------------------|------------------------|
| Estadístico de prueba      | -2.558103              | -8.521279e+00          |
| p-value                   | 0.101969               | 1.098956e-13           |
| # de retardos usados       | 9                      | 17                     |
| # de observaciones usadas  | 1280                   | 1272                   |
| Critical Value (1%)        | -3.435469              | -3.435501              |
| Critical Value (5%)        | -2.863801              | -2.863815              |
| Critical Value (10%)       | -2.567974              | -2.567981              |

#### Estacionariedad en media

- El gráfico de ACF de la serie original muestra autocorrelación persistente → indica no estacionariedad.
- Prueba de Dickey-Fuller sobre la serie original:

  - **p-value = 0.1019** → no se rechaza la hipótesis nula → **no estacionaria**.
  - Luego de una diferenciación: **p-value ≈ 1.09e-13** → **estacionaria en media**.

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_e.png" alt="Autocorrelación 1" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_e1.png" alt="Autocorrelación 2" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_e2.png" alt="Autocorrelación Parcial" height="300"/>
    </td>
  </tr>
</table>

#### Parámetros del modelo ARIMA

- Se propusieron modelos ARIMA(1,1,1), ARIMA(1,1,0), ARIMA(0,1,1) y ARIMA(2,1,1).
- También se utilizó `auto_arima` para comparación.
- Los parámetros se eligieron con base en el análisis de ACF/PACF y en los criterios AIC/BIC.

#### Comparación de modelos ARIMA

- Se evaluaron residuos y su densidad para cada modelo.
- **ARIMA(0,1,1)** presentó mejor AIC (904.588) y residuos más cercanos a ruido blanco.
- Los residuos se distribuyen en forma de campana estrecha, lo cual indica buen ajuste.
- La predicción en 2025 muestra comportamiento plano debido a la naturaleza de la serie diferenciada.

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_g.png" alt="Residuos" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_g1.png" alt="ARIMA" height="300"/>
    </td>
</table>

#### Otros modelos

| Modelo           | Captura de Tendencia     | Captura de Estacionalidad                  |
| ---------------- | ------------------------ | ------------------------------------------ |
| **ARIMA(0,1,1)** | Sí (mediante diferencia) | No                                         |
| **Prophet**      | Sí                       | Sí (semanal)                               |
| **Holt-Winters** | Sí                       | Sí (anual, aunque artificial en este caso) |
| **MLP**          | Parcialmente             | No                                         |

- **ARIMA** ofrece buen ajuste general, pero predice valores planos debido a su naturaleza.
- **Prophet** y **Holt-Winters** modelan tendencias y estacionalidades, pero no logran captar las fluctuaciones abruptas.
- **MLP** fue el único modelo que capturó parcialmente los picos observados en la serie, con bajo error de predicción.

**Gráficas comparativas**:

- Residuos y densidad de ARIMA: *ver imágenes del inciso g*.

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_h.png" alt="Prophet" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_h1.png" alt="Holt-Winters" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie1/inciso_h2.png" alt="MLP" height="300"/>
    </td>
  </tr>
</table>

### Serie de consumo de diésel

#### Inicio, fin y frecuencia de la serie

- **Inicio:** enero 2000
- **Fin:** mayo 2025
- **Frecuencia:** mensual

#### Gráfico y observaciones preliminares

- Se observa una tendencia al alza en el consumo de diésel.
- También hay presencia evidente de **estacionalidad**, especialmente en los ciclos anuales.
- La variabilidad de la serie se incrementa con el tiempo.

<div style="text-align: center;">
  <img src="../images/modelado/serie2/inciso_b.png" alt="Serie Temporal de Consumo de Combustible Tipo 'Diésel' (2000–2025)" height="300"/>
</div>

#### Descomposición de la serie

- La descomposición muestra componentes tendencia, estacionalidad y residuos bien definidos.
- La estacionalidad es anual y muy marcada.
- Los residuos parecen distribuidos de manera aleatoria sin patrones claros.

<div style="text-align: center;">
  <img src="../images/modelado/serie2/inciso_c.png" alt="Descomposición de la Variable 'diésel'" height="300"/>
</div>

#### Transformación de la serie

- Prueba de Dickey-Fuller aplicada a la serie original:

  - **Estadístico:** 2.2922
  - **p-value:** 0.999 → **no estacionaria**
- Luego de aplicar una primera diferenciación:

  - **Estadístico:** -4.3825
  - **p-value:** 0.0003 → **estacionaria en media**

| Métrica                    | Test 1     | Test 2     |
|----------------------------|------------|------------|
| Estadístico de prueba       | 2.292167   | -4.382493  |
| p-value                    | 0.998950   | 0.000319   |
| # de retardos usados        | 14         | 16         |
| # de observaciones usadas   | 290        | 288        |
| Critical Value (1%)         | -3.453102  | -3.453262  |
| Critical Value (5%)         | -2.871559  | -2.871628  |
| Critical Value (10%)        | -2.572108  | -2.572146  |

#### Estacionariedad en media

- ACF muestra autocorrelación persistente, indicando no estacionariedad.
- PACF sugiere orden bajo de modelo ARIMA.

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/modelado/serie2/inciso_e.png" alt="ACF" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie2/inciso_e1.png" alt="PACF" height="300"/>
    </td>
  </tr>
</table>

#### Parámetros del modelo ARIMA

- Se propusieron los modelos ARIMA(1,1,1), ARIMA(0,1,1) y ARIMA(2,1,0).
- Además, se utilizó `auto_arima` con componente estacional (`seasonal=True`, `m=12`).
- Los parámetros fueron seleccionados con base en los gráficos de ACF/PACF y comparación con criterios AIC.

- **Entrenamiento:** hasta diciembre 2023
- **Validación:** enero a diciembre 2024
- **Prueba:** enero a mayo 2025

#### Comparación de modelos ARIMA

- Se entrenaron y evaluaron los siguientes modelos:

  - **ARIMA(1,1,1)**
  - **ARIMA(0,1,1)**
  - **ARIMA(2,1,0)**
  - **auto_arima (modelo automático con estacionalidad)**

- Según la gráfica de comparación, **el modelo automático (`auto_arima`) se ajusta mejor** a los datos reales del conjunto de prueba.

<div style="text-align: center;">
  <img src="../images/modelado/serie2/inciso_g.png" alt="ARIMA" height="300"/>
</div>

#### Otros modelos

| Modelo           | Captura de Tendencia     | Captura de Estacionalidad       |
| ---------------- | ------------------------ | ------------------------------- |
| **ARIMA auto**   | Sí (mediante diferencia) | Sí (mediante componente SARIMA) |
| **Prophet**      | Sí                       | Sí (anual)                      |
| **Holt-Winters** | Parcialmente             | Sí (mensual, pero mal ajustada) |
| **MLP**          | Parcialmente             | No                              |

- **ARIMA automático** fue el que mejor ajustó la serie, capturando estacionalidad y tendencia.
- **Prophet** detectó adecuadamente la tendencia creciente y los ciclos anuales, pero falló ante las fluctuaciones más bruscas.
- **Holt-Winters** no logró converger correctamente; su ajuste fue limitado y requiere mejoras.
- **MLP** capturó la forma general pero con errores más altos (RMSE ≈ 65,000), sin modelar bien la estacionalidad ni los extremos.

**Gráficas comparativas**:

- Residuos y predicciones de ARIMA: *ver imágenes del inciso g*.

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/modelado/serie2/inciso_h.png" alt="Prophet" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie2/inciso_h1.png" alt="Holt-Winters" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie2/inciso_h2.png" alt="MLP" height="300"/>
    </td>
  </tr>
</table>

### Serie de importaciones de GLP

#### Inicio, fin y frecuencia de la serie

- **Inicio:** enero 2000
- **Fin:** mayo 2025
- **Frecuencia:** mensual

#### Gráfico y observaciones preliminares

- Se observa una **tendencia creciente** en las importaciones de GLP.
- La serie presenta una **estacionalidad fuerte** y una varianza creciente con el tiempo.
- Las fluctuaciones son frecuentes, con algunos picos extremos.

<div style="text-align: center;">
  <img src="../images/modelado/serie3/inciso_b.png" alt="Serie GLP" height="300"/>
</div>

#### Descomposición de la serie

- La descomposición muestra una **tendencia creciente**, **estacionalidad regular** y **residuos sin patrón definido**.
- La estacionalidad parece mensual, con repeticiones cíclicas claras.

<div style="text-align: center;">
  <img src="../images/modelado/serie3/inciso_c.png" alt="Descomposición GLP" height="300"/>
</div>

#### Transformación de la serie

- La prueba de Dickey-Fuller aplicada a la serie original arrojó un **p-value ≈ 0.928**, indicando que **no es estacionaria**.
- Luego de aplicar **logaritmo + primera diferenciación**, el **p-value ≈ 4.7e-21**, confirmando **estacionariedad en media**.

| Métrica                    | Test 1        | Test 2            |
|----------------------------|---------------|-------------------|
| Estadístico de prueba       | -0.281940     | -1.149170e+01     |
| p-value                    | 0.928023      | 4.719084e-21      |
| # de retardos usados        | 9             | 8                 |
| # de observaciones usadas   | 283           | 284               |
| Critical Value (1%)         | -3.453670     | -3.453587         |
| Critical Value (5%)         | -2.871808     | -2.871771         |
| Critical Value (10%)        | -2.572241     | -2.572222         |

#### Estacionariedad en media

- El gráfico ACF muestra autocorrelación persistente.
- El gráfico PACF sugiere orden bajo de autoregresión.

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/modelado/serie3/inciso_e.png" alt="ACF" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie3/inciso_e1.png" alt="PACF" height="300"/>
    </td>
  </tr>
</table>

#### Parámetros del modelo ARIMA

- Se propusieron los modelos ARIMA(1,1,1), ARIMA(0,1,1) y ARIMA(2,1,0).
- También se utilizó `auto_arima` con estacionalidad mensual (`seasonal=True`, `m=12`).
- Los modelos se compararon en función de su desempeño sobre el conjunto de prueba (enero–mayo 2025).

#### Comparación de modelos ARIMA

- Se observaron diferencias en precisión y forma de ajuste.
- **auto\_arima** capturó mejor la forma de la serie test.

<div style="text-align: center;">
  <img src="../images/modelado/serie3/inciso_g.png" alt="Comparación ARIMA GLP" height="300"/>
</div>

#### Otros modelos

| Modelo           | Captura de Tendencia     | Captura de Estacionalidad       |
| ---------------- | ------------------------ | ------------------------------- |
| **ARIMA auto**   | Sí (mediante diferencia) | Sí (SARIMA, mensual)            |
| **Prophet**      | Sí                       | Sí (anual)                      |
| **Holt-Winters** | Parcialmente             | Sí (mensual, pero poco preciso) |
| **MLP**          | Parcialmente             | No                              |

- **ARIMA (auto)** fue el modelo con mejor comportamiento, logrando representar tanto la estacionalidad como la tendencia creciente.
- **Prophet** detectó bien la tendencia, pero su enfoque de estacionalidad anual no se adaptó a los ciclos mensuales de la serie.
- **Holt-Winters** logró captar patrones, pero su ajuste fue débil y poco confiable.
- **MLP** (Red Neuronal) representó parcialmente la forma general de la serie, pero sin capturar la estacionalidad y con errores más altos (RMSE ≈ 0.3363).

**Gráficas comparativas**:

<table style="margin: auto; text-align: center; border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none;">
      <img src="../images/modelado/serie3/inciso_h.png" alt="Prophet GLP" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie3/inciso_h1.png" alt="Holt-Winters GLP" height="300"/>
    </td>
    <td style="border: none;">
      <img src="../images/modelado/serie3/inciso_h2.png" alt="MLP GLP" height="300"/>
    </td>
  </tr>
</table>

## 8. Predicción

### Serie de precios de gasolina regular

Se entrenaron varios modelos de predicción utilizando como conjunto de entrenamiento los datos de 2022 y 2023. La predicción se realizó para el año 2025, y se comparó contra los valores reales disponibles para ese año (enero a mayo).

Se utilizaron modelos ARIMA (manuales y automáticos), Prophet, Holt-Winters y redes neuronales (MLP). Las predicciones fueron evaluadas con métricas de error RMSE y MAE.

| Modelo       | RMSE       | MAE        |
| ------------ | ---------- | ---------- |
| ARIMA(0,1,1) | 0.1856     | 0.0637     |
| ARIMA(1,1,1) | 0.1856     | 0.0637     |
| ARIMA(1,1,0) | 0.1844     | 0.0524     |
| ARIMA auto   | 0.1864     | 0.0643     |
| MLP          | 0.1820     | 0.0649     |

Entre los modelos evaluados, MLP (red neuronal) obtuvo el mejor RMSE. Sin embargo, la diferencia entre modelos es marginal. En general, los modelos ARIMA también se ajustaron bien a la serie.

#### Predicción para el año 2025 y comparación con la realidad

La predicción para el año 2025 se realizó usando los modelos entrenados con los datos hasta 2023. Se evaluó qué tan apegadas fueron las predicciones a la realidad observada entre enero y mayo de 2025.

Los resultados muestran que los modelos lograron capturar de manera razonable la tendencia y comportamiento general de los precios. La precisión es aceptable según las métricas de error, con valores de RMSE por debajo de 0.19, lo cual refleja una predicción confiable para una serie diaria con alta variabilidad.

Los modelos ARIMA tienden a generar trayectorias más planas, mientras que MLP logra representar mejor los cambios más abruptos en precios.

### Serie de consumo de diésel

Se entrenaron modelos de predicción utilizando como conjunto de entrenamiento los datos desde el inicio de la serie hasta el año 2023. Posteriormente, se realizaron predicciones para los años 2023, 2024 y 2025, evaluando especialmente el desempeño en el año 2025 (último año disponible).

Se probaron modelos ARIMA (manuales y automáticos), Prophet, Holt-Winters y redes neuronales (MLP). La evaluación se hizo comparando las predicciones contra los datos reales disponibles para el año 2025.

| Modelo       | RMSE          | MAE           |
| ------------ | ------------- | ------------- |
| ARIMA(0,1,1) | 68,068.33     | 56,029.01     |
| ARIMA(1,1,1) | 65,357.34     | 54,151.47     |
| ARIMA(2,1,0) | 79,363.42     | 74,541.04     |
| ARIMA auto   | 32,246.90     | 24,407.50     |
| MLP          | 65,071.59     | 54,497.81     |

- El mejor modelo fue ARIMA auto, con diferencia significativa respecto a los otros, logrando los menores errores (RMSE y MAE).
- El modelo MLP tuvo desempeño cercano a ARIMA(1,1,1), pero sin superar el ajuste automático.
- Modelos ARIMA manuales mostraron errores más altos, en especial ARIMA(2,1,0).

#### Predicción para el año 2025 y comparación con la realidad

La predicción del año 2025 fue evaluada directamente contra los valores reales conocidos (enero a mayo 2025). La comparación muestra que:

- El modelo ARIMA auto logra capturar mejor el comportamiento general de la serie en 2025, probablemente gracias a su ajuste automático con estacionalidad mensual (`seasonal=True, m=12`).
- Las predicciones de MLP se acercan visualmente al patrón, pero no logran superar el ajuste estadístico del modelo ARIMA auto.
- El comportamiento real del consumo en 2025 muestra cierta recuperación tras los cambios observados en años anteriores, y los modelos captan correctamente esa tendencia.

### Serie de importaciones de GLP

Los resultados se resumen en la siguiente tabla:

| Modelo       | RMSE       | MAE        |
| ------------ | ---------- | ---------- |
| ARIMA(0,1,1) | 0.4084     | 0.3184     |
| ARIMA(1,1,1) | 0.3395     | 0.2678     |
| ARIMA(2,1,0) | 0.3995     | 0.3398     |
| ARIMA auto   | 0.2281     | 0.1947     |
| MLP          | 0.3363     | 0.2473     |

El modelo ARIMA auto obtuvo el mejor desempeño con la menor RMSE y MAE. MLP y ARIMA(1,1,1) también mostraron resultados competitivos.

#### Predicción para el año 2025 y comparación con la realidad

- ARIMA auto fue el modelo que más se acercó a los valores observados.
- MLP logró capturar algunos picos, pero fue ligeramente menos preciso.
- Los modelos ARIMA manuales mostraron comportamientos más planos y mayor error.
- La predicción fue confiable considerando la escala y estacionalidad de la serie.
