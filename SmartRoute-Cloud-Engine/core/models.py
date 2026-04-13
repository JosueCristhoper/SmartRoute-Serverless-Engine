import os
import json
from django.db import models
from azure.storage.queue import QueueClient

# Create your models here.
class Route(models.Model):
    name = models.CharField(max_length=225)
    origin_lat = models.FloatField()
    origin_long = models.FloatField()
    dest_lat = models.FloatField()
    dest_long = models.FloatField()
    # Añadimos el nuevo campo
    distance = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # Realizamos funcion para despues que guarde una Ruta Django salude
    def save(self, *args, **kwargs):

        # 1. Logica: Ponemos nombre siempre en Mayus antes de guardar
        self.name = self.name.upper()
        # 2. Guardams la ruta en la BBDD de Azure (PostgreSQL)
        # Esto va generar un ID de la ruta, lo que necesitamos para el mensaje
        super().save(*args, **kwargs)

        # 3. Preparamos el aviso para la Cola de Azure (Donde antes era la logica)
        try:
            # Traemos la llave que pusimos en .env
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

            # Conectamos con la cola que creamos en el portal de Azure ("route-requests")
            queue_client = QueueClient.from_connection_string(connection_string, "route-requests")

            # Creamos el "ticket" con el ID de la ruta
            message = {
                "route_id": self.id,
                "action": "calculate_distance"
            }

            # Enviamos el ticket convertido a texto (JSON)
            queue_client.send_message(json.dumps(message))
            print(f"DEBUG: Mensaje enviado a la cola para la ruta {self.id}")

        except Exception as e:
            # Imprimimos por si falla, pero la ruta se queda guardada.
            print(f"ERROR: enviando a la cola: {e}")
                