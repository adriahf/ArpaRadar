import requests
from datetime import datetime
import pytz
from config import DUMP1090_URL, OBSERVACIONS_FILE


def fetch_aircraft():
    """
    Obté les dades dels avions des del servidor dump1090.

    Returns:
        dict: Dades JSON amb la llista d'avions detectats.
    
    Raises:
        requests.HTTPError: En cas de resposta invàlida del servidor.
    """
    resp = requests.get(DUMP1090_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_barcelona_time():
    """
    Retorna l'hora actual a Barcelona.

    Returns:
        str: Timestamp en format YYYY-MM-DD HH:MM:SS.
    """
    tz = pytz.timezone("Europe/Madrid")  # Barcelona comparteix zona horària amb Madrid
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")


def save_observations():
    """
    Guarda una observació (llista de posicions d'avions) en un fitxer CSV.
    Cada línia conté: [timestamp] [llista latituds] [llista longituds] [llista altituds]
    """
    timestamp = get_barcelona_time()

    # Intentem obtenir les dades del receptor dump1090
    try:
        data = fetch_aircraft()
    except Exception as e:
        print(f"[ERROR] No s'han pogut obtenir les dades: {e}")
        return

    aircraft_list = data.get("aircraft", [])

    # Extraiem coordenades bàsiques de cada avió
    lats, lons, alts = [], [], []
    for plane in aircraft_list:
        lats.append(plane.get("lat"))
        lons.append(plane.get("lon"))
        alts.append(plane.get("alt_baro"))

    # Guardem la línia d'observació al fitxer (mode append)
    try:
        with open(OBSERVACIONS_FILE, "a", encoding="utf-8") as f:
            line = (
                f"{timestamp}\t"
                f"{lats}\t"
                f"{lons}\t"
                f"{alts}\n"
            )
            f.write(line)
        print(f"[{timestamp}] Dades guardades ({len(aircraft_list)} avions)")
    except Exception as e:
        print(f"[ERROR] No s'han pogut guardar les dades: {e}")
