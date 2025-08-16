# ArpaRadar: Seguiment d'avions amb receptor ADS-B

Aquest projecte permet visualitzar en temps real avions que passen pel cel de Barcelona, mostrant per pantalla d'on vénen quan travessen un espai aeri definit. Les dades es capturen mitjançant un receptor ADS-B i es processen per identificar si un avió entra dins d’un volum 3D d’interès.

---

## 🎯 Motivació

Tot va començar durant una visita amb uns amics al **mirador d'avions del Prat de Llobregat**. Ens vam entretenir consultant **d'on venien els avions amb FlightRadar**, tot intentant endevinar l'origen abans que aterressin.

Des de casa meva també es poden veure els avions que després passen pel mirador. Després d’aquella experiència, em vaig aficionar a observar les rutes i vaig decidir muntar un sistema propi per fer-ho:

- 📡 Vaig comprar un **receptor de senyal ADS-B**
- 💻 Vaig instal·lar el programari **dump1090** en un **miniPC**
- 🧠 Vaig analitzar les trajectòries dels avions en un **espai tridimensional** definit
- 🧾 Vaig programar un sistema per detectar quan un avió entra dins aquest volum
- 🧪 Finalment, vaig comprar una **tablet de segona mà a Wallapop**, pensada per ús exterior, i hi vaig desplegar una aplicació que mostra d’on venen els avions que sobrevolen aquesta zona

Aquest repositori conté tot el codi necessari per a fer-ho funcionar.

---

## 📂 Contingut del repositori

- `app.py`: servidor Flask per exposar les dades via API
- `plane_data.py`: processament dels avions, detecció dins de l’espai 3D, càlcul de posició relativa i origen
- `helpers.py`: definició del volum 3D i càlculs relacionats
- `observations.py`: script per enregistrar observacions en un fitxer
- `frontend/`: codi HTML, CSS i JS de la interfície que mostra els avions detectats
- `.env`: fitxer (no inclòs) amb la configuració personalitzada (IP del receptor, noms de fitxer, etc.)

---

## ⚙️ Requisits

- Python 3.8 o superior
- Receptor ADS-B actiu amb dump1090 accessible per IP local
- Paquets Python:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🔧 Configuració

1. **Crea un fitxer `.env`** a l’arrel del projecte:

   ```env
   DUMP1090_URL=http://[ip_del_pc]:1090/data/aircraft.json
   OBSERVACIONS_FILE=[nom_del_fitxer].csv
   ROUTE_API_URL=[URL_DE_L_API]
   ```

2. **Executa el servidor Flask**:
   ```bash
   python app.py
   ```

3. **Obre el navegador o la tablet i accedeix a** `http://[ip_del_pc]:5000`

---

## 🗺️ Funcionalitat

- Consulta contínua de la posició d’avions detectats per l’ADS-B
- Càlcul de si un avió entra dins un **volum 3D definit per coordenades i altituds**
- Si entra, es mostra per pantalla el **punt d'origen (aeroport de sortida)** en gran, per facilitar-ne la visualització des d’un dispositiu extern
- Visualització animada del moviment de l'avió dins la zona

---

## 🧪 Exemple d’ús
![Screenshot from 2025-06-18 22-29-49](https://github.com/user-attachments/assets/7bc5e0fa-2b36-40b9-8769-998f441ee510)

---

## 🔐 Privadesa

Aquest projecte utilitza dades locals. Les adreces IP i noms de fitxer estan configurats a través de variables d'entorn per evitar exposar informació sensible. Recorda **no pujar mai el `.env` a un repositori públic**.

---

## 📄 Llicència

Aquest projecte està publicat sota la llicència **GNU General Public License v3.0 (GPL-3.0)**.  
Això vol dir que **pots utilitzar, modificar i distribuir el codi lliurement**, sempre que les versions modificades **també es distribueixin com a codi obert amb la mateixa llicència**.

Per més informació, consulta el fitxer [`LICENSE`](LICENSE).
---

## 🙌 Gràcies

Inspirat per una tarda entre amics i el plaer de mirar el cel.
