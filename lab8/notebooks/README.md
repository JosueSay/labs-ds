# Uso de Docker

## Comenzar desde cero (primera vez)

```bash
# Construir la imagen y levantar contenedor
docker-compose up --build
```

* Esto construye la imagen `spark-lab` y levanta el contenedor `spark-jupyter`.
* JupyterLab quedará disponible en tu navegador en [http://127.0.0.1:8888/lab](http://127.0.0.1:8888/lab).

## Detener el contenedor (cuando termines de trabajar)

```bash
docker-compose stop
```

* Esto apaga el contenedor pero **no elimina datos**.
* Puedes levantarlo nuevamente más rápido.

## Volver a iniciar un contenedor apagado

```bash
docker-compose start
```

* Esto inicia el contenedor previamente detenido.
* Tus archivos en `/home/jovyan/work` **siguen ahí** si estás usando el volumen correcto.

## Reiniciar un contenedor (por si algo falla)

```bash
docker-compose restart
```

* Esto apaga y vuelve a encender el contenedor en un solo paso.

## Ver el estado de contenedores

```bash
docker-compose ps
```

* Te muestra qué contenedores están corriendo y sus puertos.
* Por ejemplo, `spark-jupyter` debería mostrar **Up (healthy)**.

## Entrar al contenedor para depuración

```bash
docker exec -it <CONTAINER_ID> bash
# o usando nombre del contenedor
docker exec -it spark-jupyter bash
```

* Aquí puedes ejecutar `ls`, `python`, `os.makedirs(...)`, etc.

## Parar y eliminar todo (limpieza total)

```bash
docker-compose down        # apaga y elimina contenedores y red
docker volume rm $(docker volume ls -q)   # elimina todos los volúmenes (opcional)
docker rmi spark-lab:latest              # elimina la imagen (opcional)
```

* Esto te deja como si nunca hubieras corrido el contenedor.
