import time
import requests

import helpers
import observations
from config import ROUTE_API_URL


class Airplane:
    """
    Classe que representa un avió amb la seva posició i informació de sortida.
    """
    def __init__(self, callsign, icao, latitude, longitude, altitude, departure):
        self.callsign = callsign
        self.icao = icao
        self.lat = latitude
        self.lon = longitude
        self.alt = altitude
        self.departure = departure
        self.percentage = -1  # Inicialment, fora de la zona d'interès


# Caché global d'avions identificats per ICAO
airplane_cache = {}


def get_aircraft_positions():
    """
    Obté les posicions dels avions mitjançant `dump1090` i processa
    si algun d'ells es troba dins d'una figura 3D definida.

    Retorna:
        list: Llista d'instàncies d'Airplane dins la zona d'interès.
    """
    try:
        data = observations.fetch_aircraft()
    except Exception as e:
        print(f"[ERROR] No s'ha pogut obtenir dades dels avions: {e}")
        return []

    aircrafts = []

    for aircraft in data.get("aircraft", []):
        callsign = aircraft.get('flight', '').strip()
        icao = aircraft.get("hex", "").strip()
        latitude = aircraft.get("lat")
        longitude = aircraft.get("lon")
        altitude = aircraft.get("alt_baro")

        # Validem que la posició sigui completa
        if not all(x is not None for x in [latitude, longitude, altitude]):
            continue

        # Recuperem o creem l'objecte avió
        if icao in airplane_cache:
            airplane = airplane_cache[icao]
            # Actualitzem posició
            airplane.lat = latitude
            airplane.lon = longitude
            airplane.alt = altitude
        else:
            airplane = Airplane(callsign, icao, latitude, longitude, altitude, None)
            airplane_cache[icao] = airplane

        # Comprovem si el punt està dins de la figura 3D definida
        point = (longitude, latitude, altitude)
        inside = helpers.is_point_inside_3d_figure(point, helpers.VERTICES, helpers.FACES)

        airplane.percentage = -1  # Reset
        route_info_counter = 0 # Intents per obtenir la ruta
        if inside:
            # Si no tenim info d'origen, l'intentem obtenir
            if airplane.departure is None:
                try:
                    route_info = get_route_info(callsign, latitude, longitude)
                    airport_info = route_info[0]['_airports'][0]['location']
                    airplane.departure = airport_info
                except Exception as e:
                    print(f"[ERROR] No s'ha pogut obtenir ruta per {icao}: {e}")
                    route_info_counter += 1
                    if route_info_counter > 5:
                        print("[WARNING] S'ha superat el límit d'intents per obtenir la ruta.")
                        airplane.departure = "Desconegut"

            # Només calculem el percentatge si és dins la figura
            percentage = helpers.calculate_relative_distance(point, helpers.VERTICES)
            airplane.percentage = percentage

            # Només afegim el primer avió que trobem dins la figura
            if len(aircrafts) == 0:
                aircrafts.append(airplane)

    return aircrafts


def get_route_info(callsign, lat, lng):
    """
    Fa una petició POST a adsb.im per obtenir l'origen i el destí d'un vol.

    Args:
        callsign (str): Identificador del vol
        lat (float): Latitud
        lng (float): Longitud

    Returns:
        dict: Resposta JSON de l'API amb la informació de ruta
    """
    payload = {
        "planes": [{
            "callsign": callsign.strip(),
            "lat": lat,
            "lng": lng
        }]
    }

    resp = requests.post(ROUTE_API_URL, json=payload, timeout=5)
    resp.raise_for_status()  # Llança excepció si hi ha error HTTP
    return resp.json()