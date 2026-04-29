# SmartRoute Serverless Engine 

Este repositorio contiene la arquitectura completa de **SmartRoute**, un ecosistema escalable para la gestión y procesamiento inteligente de rutas geográficas. 

El proyecto utiliza una **arquitectura desacoplada**, separando la recepción de datos (API) del procesamiento pesado (Worker Serverless) mediante sistemas de mensajería en la nube.

---

## Estructura del Ecosistema

El proyecto se divide en dos componentes principales:

* **📁 [SmartRoute-Cloud-Engine](./SmartRoute-Cloud-Engine):** El "Cerebro" administrativo. Una API robusta construida con **Django & Docker** que recibe las peticiones, gestiona la base de datos PostgreSQL en Azure y emite tickets de trabajo.
* **📁 [smartroute-worker](./smartroute-worker):** El "Motor" de cálculo. Un servicio **Serverless basado en Azure Functions** que escucha la cola de mensajes, realiza los cálculos matemáticos de rutas y actualiza los resultados de forma asíncrona.

---

## Arquitectura de Datos

1. **Client/Frontend:** Envía coordenadas de origen y destino.
2. **Django API (Producer):** Valida los datos y los coloca en una **Azure Storage Queue**.
3. **Azure Queue Storage:** Actúa como colchón de persistencia y desacoplamiento.
4. **Azure Function (Consumer):** Se dispara automáticamente al recibir un mensaje, calcula la distancia y guarda el resultado.

---

## Cómo empezar

Este proyecto está totalmente orquestado con **Docker Compose**, lo que permite levantar todo el entorno (Base de Datos, Sistema de Colas y Backend) con un solo comando.
### 1. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto basándote en el archivo de ejemplo. Este archivo centraliza la configuración tanto para el entorno local como para la conexión con servicios de Azure en la nube.

### 2. Levantar el ecosistema
Ejecuta el siguiente comando en la terminal:
```bash
docker compose up --build
```

### 3. Inicializar Base de Datos (Solo la primera vez)
Una vez que los contenedores estén corriendo, ejecuta las migraciones y crea tu usuario administrador:
```bash
docker exec -it django-backend python manage.py migrate
docker exec -it django-backend python manage.py createsuperuser
```

> **Nota:** El panel de administración estará disponible en http://localhost:8000/admin.