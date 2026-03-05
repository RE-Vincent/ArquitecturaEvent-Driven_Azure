# ArquitecturaEvent-Driven_Azure

1- Estado Registrado para el proveedor de Event Grid en la suscripción
![alt text](images/registro_eventgrid.png)
2- Creamos la función
![alt text](images/azurefunction.png)
3- En la cuenta de almacenamiento:
    1. Claves de acceso
    2. Key1
    3. Cadena de conexión (copiar)
![alt text](images/keyconexion.png)
4- Registramos la clave como variable (Produccion)
    1. Function App
    2. Configuración
    3. Variables de entorno
    4. [+]Agregar
![alt text](images/variable_key.png)
4.0.1- Registramos la clave como variable (Local - Desarrollo)
    1. en local.settings.json
    2. Agregamos NOMBRE_VARIABLE: cadena_de_conexion
