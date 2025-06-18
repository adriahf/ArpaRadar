from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from plane_data import get_aircraft_positions
import os

# --- Configuració de rutes i directoris ---

# Directori base de l'aplicació (on es troba aquest fitxer)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directori on es troba el frontend (HTML, CSS, JS)
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

# Directori d'estàtics compartits (imatges, fonts, etc.)
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

# --- Inicialització de l'aplicació Flask ---

# Servim només l'API des de Flask; els fitxers estàtics es serveixen externament
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
CORS(app)  # Permetem peticions des de qualsevol origen (CORS)

# --- Rutes del servidor ---

@app.route('/')
def index():
    """
    Ruta principal. Serveix el fitxer index.html com a entrada del frontend.
    """
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
def frontend_files(filename):
    """
    Ruta genèrica per servir fitxers del frontend (CSS, JS, fonts...).
    Permet més flexibilitat que el servidor estàtic per defecte.
    """
    return send_from_directory(FRONTEND_DIR, filename)


@app.route('/api/planes')
def plane_positions():
    """
    Endpoint de l'API que retorna la posició actual dels avions.
    La resposta és una llista de diccionaris en format JSON.
    """
    data = get_aircraft_positions()

    # Convertim els objectes a diccionaris per poder serialitzar-los
    plane_data_dict = [plane.__dict__.copy() for plane in data]
    return jsonify(plane_data_dict)


# --- Execució del servidor ---

if __name__ == '__main__':
    # Executem l'aplicació en mode debug i escoltant totes les IPs locals
    app.run(host='0.0.0.0', port=5000, debug=True)
