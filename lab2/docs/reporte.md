# Laboratorio 2 - Reporte

## Serie "Precios de Gasolina Regular"

### Análisis visual

Desde 2021 hasta mediados de 2025, con datos diarios.

1. **2021 – inicios de 2022:**
   El precio comienza en niveles bajos (\~Q22 por galón) y muestra un ascenso progresivo.

2. **2022:**
   Se registra un **aumento abrupto**, alcanzando su punto máximo cercano a **Q40.50**.
   Esta subida coincide con eventos internacionales que afectaron los precios del crudo (como la guerra en Ucrania).

3. **2023:**
   El precio desciende gradualmente, aunque se observan algunos picos intermedios que muestran una recuperación parcial.

4. **2024:**
   El precio muestra un ascenso desde 2023 pero, pero sin alcanzar los niveles de 2022.

5. **2025:**
   Los precios se **estabilizan** en un rango alrededor de Q28–Q30, sin picos extremos.

- No hay evidencia visual clara de estacionalidad (es decir, no hay patrones que se repitan todos los años o todos los meses).
- La serie es volátil en el corto plazo, con muchos cambios bruscos.
- Los precios máximos ocurren en 2022.
- Los niveles actuales (2025) son más bajos, pero aún por encima de los valores iniciales de 2021.

La serie original muestra el comportamiento crudo de los precios diarios, permitiendo observar visualmente los picos, caídas y fluctuaciones. La tendencia suaviza la serie para resaltar la dirección general del precio, confirmando una subida fuerte en 2022, seguida de una baja y cierta estabilidad hacia 2025. La estacionalidad, en este caso, no presenta patrones claros ni repetitivos, lo que indica que la serie no es estacional. Por su parte, los residuos reflejan la parte impredecible del precio. En la mayoría de los años, los puntos están cerca de cero, lo cual indica que el modelo logra explicar bien los cambios con solo la tendencia. Sin embargo, en 2022 y parte de 2023 y 2024, los residuos se dispersan considerablemente, lo que sugiere la influencia de eventos anómalos o externos, como la guerra en Ucrania o los efectos post-pandemia, que el modelo no puede prever. Incluso en 2024, especialmente al inicio del año, se observa esta dispersión, aunque disminuye hacia el final.

En la gráfica de ACF (Autocorrelación), estamos observando cómo el precio actual de la gasolina regular se relaciona con los precios de días anteriores. En el eje horizontal vemos los "lags", que representan cuántos días atrás estamos comparando. Por ejemplo, el lag 1 compara el precio de hoy con el de ayer, el lag 2 con el de hace dos días, y así sucesivamente. En el eje vertical se muestra qué tanto se parecen esos precios, usando valores entre -1 y 1 (siendo 1 una relación perfecta, 0 ninguna relación, y -1 una relación inversa).

Cada barra vertical (línea con punto arriba) representa esa relación para un día específico en el pasado. Además, hay una zona sombreada azul, que sirve como una especie de regla o umbral: si una barra está completamente dentro de esa zona, se considera que la relación no es estadísticamente significativa, es decir, que probablemente es ruido o coincidencia. Pero si una barra sobresale de la zona azul (ya sea el punto o la línea), se interpreta como una relación fuerte y real, útil para modelos de predicción.

En este caso, las primeras barras, como la del lag 1 y lag 2, sobresalen claramente de la zona azul, lo cual nos dice que el precio de hoy sí depende bastante de los precios recientes. A medida que pasan más días (lags más lejanos como el 10, 15 o 30), las barras se hacen más pequeñas y muchas quedan cubiertas por la zona azul. Esto significa que la influencia del pasado se va debilitando con el tiempo. Sin embargo, algunas barras como la del lag 30, aunque aún sobresalen parcialmente, tienen una relación más débil o menos segura. Si solo una parte de la barra sobresale, puede que haya algo de relación, pero ya no es tan fuerte ni confiable.

Este comportamiento, donde las barras empiezan altas y van bajando lentamente, es típico de una serie no estacionaria. Eso significa que el comportamiento del precio cambia a lo largo del tiempo; no sigue una estructura fija o estable. Por ejemplo, en una serie estacionaria el precio podría fluctuar siempre en torno a un mismo promedio, pero aquí vemos que hay subidas y bajadas largas, como la de 2022, probablemente por eventos como la guerra en Ucrania o la crisis post-pandemia. Por eso, antes de aplicar modelos de predicción, es recomendable transformar la serie (por ejemplo, restar el valor anterior o aplicar una "diferencia") para que sea más estable y el modelo pueda aprender mejor.

En la gráfica de PACF (Autocorrelación Parcial), estamos observando qué tan directamente se relaciona el precio actual de la gasolina regular con los precios de días anteriores, pero eliminando la influencia de los días intermedios. Por ejemplo, el lag 5 aquí nos dice si el precio de hace cinco días tiene una conexión directa con el de hoy, sin importar lo que pasó entre esos días. Esto es distinto del ACF, que mide la relación acumulada incluyendo todos los lags intermedios.

El eje horizontal muestra los desfases en días (lags), y el eje vertical indica el grado de relación parcial entre el precio actual y el de esos días, con valores entre -1 y 1. Cada barra vertical representa esa relación para un día específico. También vemos una zona azul que indica el rango en el que una correlación no es estadísticamente confiable. Si una barra queda completamente dentro de esa zona, quiere decir que el día pasado probablemente no afecta directamente al precio actual. Si una barra sobresale, significa que ese día tiene una relación directa y útil.

En esta gráfica, solo el lag 1 sobresale con claridad de la banda azul, lo que indica que el precio de hoy tiene una relación directa fuerte con el de ayer. Algunos lags sobresalen un poco, pero su efecto es más débil y los que están dentro de la banda azul o muy cerca de ella significa que no aportan información directa confiable para predecir el valor actual.

Este comportamiento nos dice que, aunque el precio de la gasolina puede verse influido por lo que pasó antes, solo los primeros días tienen un impacto directo real. A medida que nos alejamos en el tiempo, esa influencia desaparece o se mezcla con ruido. Esta gráfica es muy útil para saber cuántos valores pasados conviene usar si vamos a aplicar modelos predictivos como ARIMA, porque nos ayuda a elegir los componentes autoregresivos (AR). En este caso, usar solo el lag 1.

Una vez que confirmamos que la serie no es estacionaria, lo siguiente que se debe hacer es aplicar una transformación para que el modelo pueda trabajar con datos más estables. En este caso, la transformación elegida fue la diferenciación, que consiste en calcular el cambio entre un día y el siguiente. Al aplicar esta transformación, observamos que el comportamiento de la serie se estabiliza: ya no tiene una tendencia fuerte ni varianza cambiante, lo cual facilita el modelado. Esto se confirmó mediante una segunda prueba de Dickey-Fuller sobre la serie ya diferenciada. En esta nueva prueba, el estadístico de prueba fue mucho menor que los valores críticos, y el p-value fue extremadamente bajo (cercano a cero), lo que indica que ahora sí se puede considerar estacionaria.

Con esta nueva serie transformada, ya se puede aplicar un modelo como ARIMA, que requiere que los datos sean estacionarios para funcionar correctamente. Este modelo no se entrena con los valores originales del precio, sino con los cambios entre días. Entonces, una vez que se hacen predicciones, esas predicciones estarán en forma de diferencias (por ejemplo, +0.12, -0.10, etc.). Para obtener los valores reales del precio, es necesario tomar el último valor conocido real y sumarle las predicciones de forma acumulativa. Es decir, si el precio real fue Q30.00 y el modelo predice +0.15, entonces el nuevo precio estimado sería Q30.15. Para el siguiente día, se suma la siguiente diferencia al valor anterior, y así sucesivamente.
