// Objecte que emmagatzema les instàncies dels avions actius a la pantalla
let planes = {};

// Element on es mostra el text de sortida del vol
const departureElement = document.getElementById('departure-info');

// Funció principal que s'executa periòdicament per actualitzar els avions
async function updatePlanes() {
  try {
    const response = await fetch('/api/planes');
    const planeData = await response.json();

    // Esborrem el text si no hi ha avions actius
    departureElement.textContent = '';

    planeData.forEach(plane => {
      if (plane.percentage === -1) {
        // Si el percentatge és -1, vol dir que l'avió ha desaparegut i cal eliminar-lo
        if (planes[plane.id]) {
          planes[plane.id].remove();
          delete planes[plane.id];
        }
      } else {
        // Actualitzem el text amb el nom de la sortida
        departureElement.textContent = plane.departure;

        // Si l'avió no existeix encara al DOM, el creem
        if (!planes[plane.id]) {
          planes[plane.id] = createPlaneElement(plane.id);
        }

        // Actualitzem la posició de l'avió segons el percentatge
        movePlane(planes[plane.id], plane.percentage);
      }
    });
  } catch (error) {
    // Registre d'errors per facilitar el debugging
    console.error('Error actualitzant els avions:', error);
  }
}

/**
 * Crea un element <img> per representar un avió.
 * @param {string} id - Identificador únic de l'avió
 * @returns {HTMLElement} - L'element img creat
 */
function createPlaneElement(id) {
  const plane = document.createElement('img');
  plane.id = id;
  plane.src = '../static/images/plane.png';
  plane.classList.add('plane');

  // Afegim l'avió al contenidor d'animació
  document.getElementById('animation-container').appendChild(plane);
  return plane;
}

/**
 * Mou l'avió horitzontalment segons un percentatge del recorregut.
 * @param {HTMLElement} planeElement - Element DOM de l'avió
 * @param {number} percentage - Percentatge del recorregut (0 a 100)
 */
function movePlane(planeElement, percentage) {
  const container = planeElement.parentElement;

  // Calculem la posició horitzontal en píxels a partir del percentatge
  const xPosition = (percentage / 100) * container.clientWidth;

  // Utilitzem transform per millors rendiments (acceleració GPU)
  planeElement.style.transform = `translateX(${xPosition}px)`;
}

// Llança la funció d'actualització cada segon
setInterval(updatePlanes, 1000);
