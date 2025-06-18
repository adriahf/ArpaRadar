# config.py

from dotenv import load_dotenv
import os

# Carrega variables d'entorn del fitxer .env
load_dotenv()

# Assigna les variables
DUMP1090_URL = os.getenv("DUMP1090_URL")
OBSERVACIONS_FILE = os.getenv("OBSERVACIONS_FILE")
ROUTE_API_URL = os.getenv("ROUTE_API_URL")

# Validació opcional per evitar errors en producció
if not DUMP1090_URL or not OBSERVACIONS_FILE or not ROUTE_API_URL:
    raise ValueError("Falten variables d'entorn al fitxer .env")