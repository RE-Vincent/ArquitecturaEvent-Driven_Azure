import azure.functions as func
import logging
import pandas as pd
from azure.storage.blob import BlobServiceClient
import io
import os

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="azevent")
def ProcessClientesJson(azevent: func.EventGridEvent):
    data = azevent.get_json()
    source_url = data.get('url') # Ejemplo: .../landingzone/clientes/archivo.json
    
    if not source_url or "/clientes/" not in source_url:
        return

    # 1. Configuración de conexiones
    # Usa la Connection String de tu ADLS (puedes ponerla en Variables de Entorno)
    connection_string = os.getenv("ADLS_CONNECTION")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    try:
        # 2. Leer el JSON original
        # Extraemos el nombre del contenedor y la ruta del blob de la URL
        parts = source_url.split('/')
        container_name = "landingzone"
        blob_path = "/".join(parts[parts.index(container_name)+1:])
        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
        json_data = blob_client.download_blob().readall()
        df = pd.read_json(io.BytesIO(json_data))

        # 3. DEFINICIÓN DEL ESQUEMA (Transformación)
        # Forzamos tipos de datos para que el Parquet sea consistente
        df['cliente_id'] = df['cliente_id'].astype(int)
        df['nombre'] = df['nombre'].astype(str)
        df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
        df['monto_compra'] = df['monto_compra'].astype(float)

        # 4. Convertir a Parquet en memoria
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
        parquet_buffer.seek(0)

        # 5. Escribir en la carpeta 'processed'
        target_path = blob_path.replace(".json", ".parquet")
        target_blob_client = blob_service_client.get_blob_client(
            container="processed", 
            blob=f"clientes_parquet/{target_path}"
        )
        target_blob_client.upload_blob(parquet_buffer, overwrite=True)
        
        logging.info(f"Éxito: Archivo convertido a Parquet en processed/clientes_parquet/")

    except Exception as e:
        logging.error(f"Error procesando el archivo: {str(e)}")
