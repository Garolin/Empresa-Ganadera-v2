import os
import pyodbc
from dotenv import load_dotenv

# Carga las variables desde el archivo .env
load_dotenv()

def probar_conexion():
    # Lee los valores del archivo .env
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")

    # Muestra en consola qué valores leyó (para confirmar que cargó el .env)
    print(f"Servidor obtenido: {server}")
    print(f"Base de datos obtenida: {database}\n")

    if not server or not database:
        print("❌ Error: No se pudieron leer las variables del archivo .env.")
        print("Asegúrate de que el archivo se llame '.env' y de haber guardado los cambios (Ctrl + S).")
        return

    # Cadena de conexión con Autenticación de Windows
    conexion_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    try:
        conexion = pyodbc.connect(conexion_str)
        print("✅ ¡Conexión exitosa a la base de datos !")
        conexion.close()
    except Exception as e:
        print(f"❌ Error al conectar con SQL Server: {e}")

if __name__ == "__main__":
    probar_conexion()