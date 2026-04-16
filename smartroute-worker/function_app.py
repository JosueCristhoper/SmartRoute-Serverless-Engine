import azure.functions as func
import logging

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
    except Exception as e:
        logging.error(f"Error al decodificar: {e}")

    