import azure.functions as func
import logging
import psycopg2
import os 
import json
import math

app = func.FunctionApp()

@app.function_name(name="SmartRouteWorker") 
@app.queue_trigger(arg_name="msg", queue_name="route-requests", connection="AzureWebJobsStorage")
def main(msg: func.QueueMessage):
    logging.warning("--- NUEVO ENCARGO RECIBIDO ---")

    try:
        body_message = msg.get_body().decode("utf-8")
        data = json.loads(body_message)
        route_id = data.get("route_id")
    except Exception as e:
        logging.error(f"Error al leer mensaje: {e}")
        return 
    
    try:
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
            lat1_raw, lon1_raw, lat2_raw, lon2_raw = row

            # --- INICIO FORMULA DE HAVERSINE ---
            lon1, lat1 = math.radians(float(lon1_raw)), math.radians(float(lat1_raw))
            lon2, lat2 = math.radians(float(lon2_raw)), math.radians(float(lat2_raw))

            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))

            distance = c * 6371

            final_distance = round(distance, 2)

            # GUARDAMOS 
            cursor.execute("UPDATE core_route " \
                           "SET distance = %s " \
                           "WHERE id = %s", (final_distance, route_id))
            
            # CONFIRMACION
            conn.commit()
            logging.warning(f"Confirmacion: Ruta {route_id} calculada en {final_distance} Km")
        
        else:
            logging.error(f"Error: El ID {route_id} no existe en la base de datos.")

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error en PostgreSQL: {e}")

    