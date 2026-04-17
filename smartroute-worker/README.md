# SmartRoute Worker 

Este componente es el motor de procesamiento asíncrono del ecosistema SmartRoute. Es una **Azure Function** ejecutándose en un contenedor Docker que procesa tareas de cálculo geográfico.

## Tecnologías
* **Python 3.11**
* **Azure Functions Core Tools v4**
* **Docker**
* **Psycopg2** Conexión directa a PostgreSQL en Azure.
* **Math**: Procesamiento de trigonometría esférica.

## Lógica de Procesamiento
El worker implementa el **Algoritmo de Haversine**, que permite calcular la distancia ortodrómica entre dos puntos en una esfera (la Tierra) a partir de sus longitudes y latitudes, con una precisión de dos decimales.

## Configuración Local
1. Crea un archivo `.env.worker` basado en tus credenciales de Azure.
   - `AzureWebJobsStorage`: Cadena de conexión a Azure.
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Credenciales de la base de datos.
2. Asegúrate de que el `host.json` tenga el encoding en `none`.

## Comandos Docker
Para construir y ejecutar el worker localmente:

```bash
# Construir imagen
docker build -t smartroute-worker-image .

# Ejecutar contenedor
docker run --name worker-en-vivo --rm --env-file .env.worker smartroute-worker-image