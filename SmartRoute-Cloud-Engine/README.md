# SmartRoute Cloud Engine 

Este es el backend oficial del proyecto **SmartRoute**, un motor en la nube diseñado para gestionar, calcular y almacenar rutas geográficas. Está construido con una arquitectura moderna utilizando contenedores y bases de datos gestionadas en la nube.

---

##  Stack Tecnológico

* **Framework:** Django 6.0.3 (Python 3.12)
* **Base de Datos:** PostgreSQL alojado en **Microsoft Azure**
* **Contenedores:** Docker & Docker Desktop
* **API REST:** Django REST Framework
* **Variables de Entorno:** `python-dotenv`
* **CORS (Preparación API):** `django-cors-headers`
* **SDK Cloud:** `azure-storage-queue` (Para mensajería asíncrona con Azure)

---

##  Fases del Proyecto

### Fase A: Infraestructura y Base de Datos (Completada)
1.  **Inicialización de Django:** Creación del proyecto base (`myproject`) y la aplicación principal (`core`).
2.  **Modelado de Datos:** Creación del modelo `Route` con campos geográficos (latitud/longitud para origen y destino) y marcas de tiempo automáticas.
3.  **Dockerización:** Configuración de un entorno reproducible mediante `Dockerfile` (instalando dependencias del sistema como `libpq-dev` y `gcc` para compilar conectores de Postgres).
4.  **Conexión a la Nube:** Transición desde la base de datos local SQLite (`db.sqlite3`) hacia un servidor **PostgreSQL en Azure**, asegurando la conexión mediante variables de entorno (`.env`).
5.  **Persistencia y Administración:** Migraciones ejecutadas con éxito en la nube y creación del superusuario para gestionar los datos a través del panel de administración de Django (`/admin`).

### Fase B: API REST (Completada)
1.  **Django REST Framework:** Instalación e integración del framework para habilitar capacidades de API.
2.  **Serialización (`serializers.py`):** Creación de un `ModelSerializer` para traducir los objetos de PostgreSQL a formato estándar JSON.
3.  **Controladores (`views.py`):** Implementación de un `ModelViewSet` para exponer automáticamente operaciones CRUD (Crear, Leer, Actualizar, Borrar).
4.  **Enrutamiento (`urls.py`):** Configuración de un `DefaultRouter` para la generación dinámica y estructurada de los endpoints de la API.

### Fase C: Lógica de Negocio y Arquitectura Asíncrona (En Progreso)
* **Lógica Matemática:** Implementación y validación de la fórmula de Haversine para calcular distancias exactas en kilómetros entre dos coordenadas geográficas.
* **Desacoplamiento Cloud:** Configuración de **Azure Storage Queues** (Colas de Almacenamiento) para extraer el cálculo matemático de Django y procesarlo de forma asíncrona en la nube.
* Configuración de CORS para permitir conexiones seguras desde el frontend (React).

---

## Cómo ejecutar el proyecto en local

Para levantar este proyecto, ya no necesitas construir imágenes manualmente; todo está automatizado a través de **Docker Compose**.

### 1. Variables de Entorno
Asegúrate de tener el archivo `.env` en la raíz del proyecto (al mismo nivel que el archivo `docker-compose.yml`). Este archivo centraliza la configuración para los contenedores y los servicios de **Azure**.

### 2. Ejecución con Docker Compose
Desde la terminal en la raíz del repositorio, ejecuta el siguiente comando:

```bash
docker compose up web
```
### 3. Gestión del Contenedor
Para realizar tareas administrativas dentro del contenedor de Django una vez esté en marcha:
* **Ejecutar Migraciones:** `docker exec -it django-backend python manage.py migrate`
* **Crear Superusuario:** `docker exec -it django-backend python manage.py createsuperuser`
* **Ver Logs en tiempo real:** `docker compose logs -f web`

### Accesos Directos
* El panel de administración estará disponible en: http://localhost:8000/admin
* API REST (Datos en formato JSON): http://localhost:8000/api/routes/
