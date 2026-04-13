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

Cada componente tiene sus propias instrucciones de configuración:
1. Revisa el README del [Backend](./SmartRoute-Cloud-Engine) para levantar la API con Docker.
2. Revisa el README del [Worker](./smartroute-worker) (Próximamente) para configurar el entorno serverless.