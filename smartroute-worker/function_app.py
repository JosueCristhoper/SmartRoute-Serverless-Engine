import azure.functions as func
import logging
import psycopg2
import os 
import json

# Instanciamos la app
app = func.FunctionApp()

@app.function_name(name="SmartRouteWorker") # Nombre unico 
@app.queue_trigger(arg_name="msg", queue_name="route-requests", connection="AzureWebJobsStorage")
def main(msg: func.QueueMessage):
    logging.warning("--- EL WORKER HA DESPERTADO!!! ---")

    try:
        # Aqui es donde se leee el contenido del envio
        body_message = msg.get_body().decode("utf-8")
        logging.warning(f"Datos recibidos de Django: {body_message}")

        # 2. Convertimos el texto en diccionario para sacar solo el numero ID
        data = json.loads(body_message)
        route_id = data.get("route_id")
        logging.warning(f"Preparando motores para la ruta ID: {route_id}")
    except Exception as e:
        logging.error(f"Error al decodificar: {e}")
        return # Por si falla la lectura, lo paramos
    
    # 3. Tocamos la puerta de PostgreSQL
    try:
        logging.warning("Intentando conectar a la base de datos...")
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            sslmode="require"
        )
        # Si azure nosd deja entrar ...
        logging.warning("CONEXION EXITOSA A POSTGRESQL !!!")
        # Y por ultimo procedemos a desconectarnos ...
        conn.close()
    
    except Exception as e:
        logging.error(f"Error conectando a PostgreSQL: {e}")

    