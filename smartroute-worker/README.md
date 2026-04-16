# SmartRoute Worker 

Este componente es el motor de procesamiento asíncrono del ecosistema SmartRoute. Es una **Azure Function** ejecutándose en un contenedor Docker que procesa tareas de cálculo geográfico.

## Tecnologías
* **Python 3.11**
* **Azure Functions Core Tools v4**
* **Docker**
* **Psycopg2** (Próximamente para PostgreSQL)

## Configuración Local
1. Crea un archivo `.env.worker` basado en tus credenciales de Azure.
2. Asegúrate de que el `host.json` tenga el encoding en `none`.

## Comandos Docker
Para construir y ejecutar el worker localmente:

```bash
# Construir imagen
docker build -t smartroute-worker-image .

# Ejecutar contenedor
docker run --name worker-en-vivo --rm --env-file .env.worker smartroute-worker-image