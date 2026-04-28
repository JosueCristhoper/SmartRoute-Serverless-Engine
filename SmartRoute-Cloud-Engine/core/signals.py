import os
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from azure.storage.queue import QueueClient
from .models import Route

# Este es el Sensor
# @receiver significa: Ejecuta cuando ocurra un post_save (guardado) en el modelo Route
@receiver(post_save, sender=Route)
def send_route_to_queue(sender, instance, created, **kwargs):
    
    # IMPORTANTE: Solo enviamos el mensaje si la ruta es recien creada (create==True)
    # Si solo estamos editando el nombrem no queremos vovler a calcular la distancia.
    if created:
        try:
            # 1. Leemos los datos que esta en el .env
            conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            queue_name = os.getenv("AZURE_QUEUE_NAME")

            # 2. Preparamos el cliente para conectar con Azurite
            # El paramatro "message_encode_policy" asegura que el texto se envie bien
            from azure.storage.queue import TextBase64EncodePolicy
            queue_client = QueueClient.from_connection_string(
                conn_str,
                queue_name,
                message_encode_policy=TextBase64EncodePolicy()
            )

            # Añadimos estas lienas de codigo para asegurar que si la cola no existe en Azurite, la cree al momento.
            try:
                queue_client.create_queue()
            except Exception:
                # Si ya existe ignoramos el error y seguimos
                pass

            # 3. Creamos el mensaje, que es la nota para el Worker
            # Solo se pasa el ID para que el Worker busque la ruta en la BBDD
            message = {
                "route_id": instance.id,
                "action": "calculate_distance"
            }

            # 4. Metemos la nota en la cola
            queue_client.send_message(json.dumps(message))

            print(f"(DEBUG) Mensaje enviado a la cola para la ruta ID: {instance.id}")

        except Exception as e:
            print(f"(ERROR) No se pudo enviar el mensaje a la cola: {e}")