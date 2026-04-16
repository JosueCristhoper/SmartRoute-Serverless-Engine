# 1. Usamos S.O que ya traiga Python 3.11 y Azure
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# 2. Donde vamos a poner el codigo dentro de esa maquina virtual
WORKDIR /home/site/wwwroot

# 3. Copiamos la lista de librerias que tenemos en requirements.txt y lo instalamos dentro del contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamos todo el contenido de la carpeta actual dentro del contenedor
COPY . .

# 5. Instrucciones finales para que el motor sepa que es una Azure Function
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true \
    FUNCTIONS_WORKER_RUNTIME=python
