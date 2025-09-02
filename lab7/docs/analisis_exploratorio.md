# Análisis exploratorio

El análisis inició con preguntas guía para orientar la selección de datos y avanzar hacia la identificación de los campos más útiles para el estudio posterior. En este proceso se priorizaron las variables que aportan información relevante:

* **Época de lluvia y horarios**: `date` → análisis de series por hora/semana/mes para identificar picos de atascos y variaciones estacionales.
* **Áreas más congestionadas**: `place/coordinates` cuando están disponibles; en su ausencia, extracción desde `raw_content` (zonas, calles) complementada con conteos y visualización en mapas.
* **Persistencia de puntos críticos**: combinación de `date` y ubicaciones inferidas para evaluar la estabilidad temporal de los "hotspots".
* **Red e influencers**: campos `mentioned_*`, `in_reply_*`, `has_quote`/`quoted_*` junto con `followers_count` para construir grafos, analizar centralidades, comunidades y cuentas clave.
* **Relevancia de eventos**: métricas de interacción (`retweet/like/quote/view`) para priorizar incidentes y validar patrones de interés.

A partir de este filtrado, se seleccionaron las siguientes columnas para el análisis:

```csv
tweet_id, date, user_id, username, followers_count, friends_count, statuses_count, raw_content, reply_count, retweet_count, like_count, quote_count, conversation_id, hashtags, mentioned_users, mentioned_users_ids, view_count, place, coordinates, in_reply_to_tweet_id, in_reply_to_user_id, in_reply_to_username, has_quote, quoted_tweet_id, quoted_user_id, quoted_username
```

La selección se fundamentó en la revisión de distintos tweets que contenían información completa o, en su defecto, aquellos con mayor riqueza de atributos. Entre ellos destacan los tweets con identificadores:
`1832855104464290053`, `1834236045598056867`.

## Identificación y tiempo

* **tweet_id**: ID único del tweet.
  *Sirve para* deduplicar, indexar y unir con otras tablas.
* **date**: fecha y hora UTC.
  *Sirve para* series temporales (picos por hora/día), relacionar con temporada de lluvias y cambios a lo largo del año.

## Autor (perfil del nodo)

* **user_id, username**: identifican al autor.
  *Sirve para* construir nodos de la red y etiquetar resultados.
* **followers_count, friends_count, statuses_count**: magnitudes del autor.
  *Sirve para* contexto de influencia potencial (p. ej., comparar engagement relativo: likes/followers).

## Contenido (texto y temas)

* **raw_content**: texto original.
  *Sirve para* tokenización, extracción de toponimia ("z 16", calzadas), tópicos y sentimiento (no mezclar con quoted).
* **hashtags**: lista de temas marcados.
  *Sirve para* temas frecuentes y co-ocurrencias (wordclouds, top hashtags).

## Interacciones del tweet (engagement)

* **reply_count, retweet_count, like_count, quote_count, view_count**: métricas de respuesta del público.
  *Sirve para* medir impacto/alcance, priorizar eventos relevantes y comparar periodos.

## Conversaciones e hilos

* **conversation_id**: agrupa tweets del mismo hilo.
  *Sirve para* reconstruir discusiones y detectar temas "calientes".
* **in_reply_to_tweet_id, in_reply_to_user_id, in_reply_to_username**: relaciones de respuesta.
  *Sirve para* aristas "reply" en la red (autor -> destinatario).

## Red de menciones

* **mentioned_users, mentioned_users_ids**: usuarios mencionados en el texto.
  *Sirve para* aristas "mention" (autor -> mencionados), detectar cuentas/medios más aludidos y subredes temáticas.

## Ubicación (cuando exista o se infiera)

* **place, coordinates**: geotag oficial (suele ser null).
  *Sirve para* mapeo directo; cuando es null, el **raw_content** permite inferir zonas/avenidas (z 16, etc.) y luego unir a polígonos/centroides.

## Citas (quote)

* **has_quote** (0/1), **quoted_tweet_id, quoted_user_id, quoted_username**: vínculo a un tweet citado.
  *Sirve para* aristas "quote" (autor -> citado), identificar fuentes amplificadas (medios/personas) y medir centralidad por citas.
  *Nota:* el contenido del citado **no** se mezcla con el `raw_content` del autor; se usa solo para la **red** e influencia.
