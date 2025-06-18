import numpy as np

# --- Definició de la figura 3D mitjançant vèrtexs i cares ---

# Vèrtexs (longitud, latitud, altitud) de dues figures rectangulars superposades
VERTICES = [
    # Primer conjunt (capa inferior, altitud 900–1500)
    (2.1853, 41.3377, 900),     # V0
    (2.1898, 41.3147, 900),     # V1
    (2.1853, 41.3377, 1500),    # V2
    (2.1898, 41.3147, 1500),    # V3

    # Segon conjunt (capa superior, altitud 2000–3000)
    (2.2726, 41.3698, 2000),    # V4
    (2.2939, 41.3530, 2000),    # V5
    (2.2726, 41.3698, 3000),    # V6
    (2.2939, 41.3530, 3000)     # V7
]

# Cares de la figura, definides com llistes de 4 vèrtexs cadascuna
FACES = [
    # Cares del primer bloc
    [VERTICES[0], VERTICES[1], VERTICES[3], VERTICES[2]],  # Cara frontal
    [VERTICES[0], VERTICES[2], VERTICES[6], VERTICES[4]],  # Connexió esquerra
    [VERTICES[1], VERTICES[3], VERTICES[7], VERTICES[5]],  # Connexió dreta

    # Cares del segon bloc
    [VERTICES[4], VERTICES[5], VERTICES[7], VERTICES[6]],  # Cara posterior

    # Cares de connexió entre blocs
    [VERTICES[2], VERTICES[3], VERTICES[7], VERTICES[6]],  # Pont superior
    [VERTICES[0], VERTICES[1], VERTICES[5], VERTICES[4]]   # Pont inferior
]


def is_point_inside_3d_figure(point, vertices, faces):
    """
    Comprova si un punt (lon, lat, alt) està dins d’una figura 3D tancada.

    Args:
        point (tuple): (longitud, latitud, altitud)
        vertices (list): llista de vèrtexs que defineixen la figura
        faces (list): llista de cares (cada cara és una llista de 4 vèrtexs)

    Returns:
        bool: True si el punt és dins de la figura, False en cas contrari
    """
    x, y, z = point

    # Càlcul del centre geomètric per establir la direcció de les normals
    centroid = (
        sum(v[0] for v in vertices) / len(vertices),
        sum(v[1] for v in vertices) / len(vertices),
        sum(v[2] for v in vertices) / len(vertices)
    )

    for face in faces:
        v0, v1, v2 = face[:3]

        # Vectors dins del pla de la cara
        vec1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
        vec2 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])

        # Producte vectorial per obtenir el vector normal del pla
        A = vec1[1] * vec2[2] - vec1[2] * vec2[1]
        B = vec1[2] * vec2[0] - vec1[0] * vec2[2]
        C = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        D = - (A * v0[0] + B * v0[1] + C * v0[2])

        # Comprovació de la direcció de la normal (ha de mirar cap enfora)
        centroid_val = A * centroid[0] + B * centroid[1] + C * centroid[2] + D
        if centroid_val > 0:
            A, B, C, D = -A, -B, -C, -D

        # Si el punt està fora d’alguna cara, ja no és dins la figura
        point_val = A * x + B * y + C * z + D
        if point_val > 1e-6:  # Tolerància per errors de coma flotant
            return False

    return True


def calculate_relative_distance(point, vertices):
    """
    Calcula la posició relativa (en percentatge 0–100%) d’un punt
    al llarg de la línia que uneix els centres dels dos blocs.

    Args:
        point (tuple): (longitud, latitud, altitud)

    Returns:
        float: Percentatge al llarg del recorregut (des del bloc superior fins al bloc inferior)
    """
    # Centres dels dos blocs
    center_first = np.mean(vertices[0:4], axis=0)
    center_second = np.mean(vertices[4:8], axis=0)

    # Vectors per al càlcul de projecció
    A = np.array(center_second)  # Inici (0%)
    B = np.array(center_first)   # Final (100%)
    P = np.array(point)          # Punt a avaluar

    AB = B - A
    AP = P - A

    # Projectem el punt sobre el vector AB
    t = np.dot(AP, AB) / np.dot(AB, AB)
    t_clamped = max(0.0, min(1.0, t))  # Assegurem rang [0, 1]

    # Mapeig per visualització (ajusta zones visibles/parcials)
    position_calibrated = map_percentage_to_display(t_clamped * 100)

    return int(np.round(position_calibrated))


def map_percentage_to_display(percentage):
    """
    Ajusta el percentatge per mostrar-lo a pantalla de forma visualment progressiva.

    Args:
        percentage (float): Percentatge original (de 0 a 100)

    Returns:
        int: Percentatge ajustat per visualització
    """
    # Interpolació amb punts de control per a una visualització més natural
    percentage_display = np.interp(
        percentage,
        [-1, 0, 32, 48, 100],
        [-1, 0, 8, 30, 100]
    )
    return int(np.round(percentage_display))
