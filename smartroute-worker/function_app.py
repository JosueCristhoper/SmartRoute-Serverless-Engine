import azure.functions as func
import logging
import psycopg2
import os 
import json
import math # <-- Para la formula de Haversine

# Instanciamos la app
app = func.FunctionApp()

@app.function_name(name="SmartRouteWorker") 
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
    except Exception as e:
        logging.error(f"Error al decodificar: {e}")
        return 
    
    # 3. Tocamos la puerta de PostgreSQL
    try:
        logging.warning("Conectando a la base de datos...")
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            sslmode="require"
        )
        cursor = conn.cursor()

        # Buscamos coordenadas
        cursor.execute("SELECT origin_lat, origin_long, dest_lat, dest_long " \
                       "FROM core_route " \
                       "WHERE id = %s", (route_id,))
        row = cursor.fetchone()

        if row:
            # Aseguramos que sean Float
            lat1_raw, lon1_raw, lat2_raw, lon2_raw = row

            # --- INICIO FORMULA DE HAVERSINE ---
            # 1. Convertimos grados a radianes
            lon1, lat1 = math.radians(float(lon1_raw)), math.radians(float(lat1_raw))
            lon2, lat2 = math.radians(float(lon2_raw)), math.radians(float(lat2_raw))

            # 2. Formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))

            # 3. Se procede a multiplicar por el radio de la tierra en Km
            distance = c * 6371

            # Se procede a redondear a 2 decimales ...
            final_distance = round(distance, 2)
            logging.warning(f"Calculo Haversine completado: {final_distance} Km")

            # GUARDAMOS el resultado
            cursor.execute("UPDATE core_route " \
                           "SET distance = %s " \
                           "WHERE id = %s", (final_distance, route_id))
            
            # CONFIRMACION de los cambios
            conn.commit()
            logging.warning(f"Distancia ({final_distance} Km) guardada en PostgreSQL")
        
        else:
            logging.error("No se encontro la ruta en la base de datos.")

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error conectando a PostgreSQL: {e}")

    