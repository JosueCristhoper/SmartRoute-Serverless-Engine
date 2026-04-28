import os
from django.db import models

class Route(models.Model):

    # Definicion de las opciones para el estado
    STATUS_CHOICES = [
        ("PENDING", "Procesando"),
        ("COMPLETED", "Completado"),
        ("FAILED", "Error"),
    ]

    name = models.CharField(max_length=225)
    origin_lat = models.FloatField()
    origin_long = models.FloatField()
    dest_lat = models.FloatField()
    dest_long = models.FloatField()
    # Añadimos el nuevo campo
    distance = models.FloatField(null=True, blank=True)
    # Añadimos nuevo campo: Por defecto sera "PENDING"
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default = "PENDING"
    )

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Actualizamos el String para ver el estado en el admin de Django
        return f"{self.name} ({self.status})"

    # Realizamos funcion para despues que guarde una Ruta Django salude
    def save(self, *args, **kwargs):

        # 1. Logica: Ponemos nombre siempre en Mayus antes de guardar
        self.name = self.name.upper()
        # 2. Guardams la ruta en la BBDD de Azure (PostgreSQL)
        # Esto va generar un ID de la ruta, lo que necesitamos para el mensaje
        super().save(*args, **kwargs)
                