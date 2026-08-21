import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")

    conexion_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conexion_str)