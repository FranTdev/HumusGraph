# Monitor de Vermicompost (Open Source)

Este proyecto es una aplicación web fullstack para monitorear datos de sensores de vermicompost. Te permite desplegar tu propio servidor central donde tus microcontroladores (ej. ESP32, Arduino, Raspberry Pi) pueden enviar datos de temperatura, humedad y pH del sustrato.

## 🛠️ Tecnologías Utilizadas

- **Backend**: FastAPI (Python) + SQLAlchemy + Base de datos (MySQL o SQLite)
- **Frontend**: React + Vite + Recharts + Tailwind CSS
- **Integraciones**: Soporta variables de entorno y consulta a la API de Meteostat para clima exterior.

## 🚀 Guía de Instalación para tu propio entorno

Sigue estos pasos para arrancar el proyecto de manera local o en un servidor dedicado.

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/HumusGraph.git
cd HumusGraph
```

### 2. Configurar Variables de Entorno (IMPORTANTE)

Para evitar exponer contraseñas y claves privadas, este proyecto usa un archivo `.env` que interactúa con las credenciales de base de datos y APIs externas.

1. En la carpeta raíz del proyecto, copia el archivo `.env.example` y nómbralo `.env`:
   ```bash
   cp .env.example .env
   ```
2. Abre el archivo `.env` que acabas de crear y completa la información de tus propias credenciales:
   ```env
   # Credenciales de Base de datos MySQL o archivo SQLite local
   MYSQL_URL="mysql+pymysql://USUARIO:CONTRASEÑA@TU_HOST_O_LOCALHOST/NOMBRE_BD"
   SQLITE_URL="sqlite:///./local_storage.db"
   
   # Crea tu cuenta gratuita en RapidAPI y busca 'Meteostat' para tu key:
   RAPIDAPI_KEY="tu_propia_key_de_rapidapi"
   WEATHER_LAT="3.513" # Latitud de donde tengas tu compostera
   WEATHER_LON="-76.608" # Longitud
   ```

*(Nota: el archivo `.env` está en el `.gitignore` así que nunca se subirá públicamente).*

### 3. Ejecutar el Backend (Servidor)

Abre una terminal en la raíz del proyecto.

```bash
# 1. Ve a la carpeta backend e instala dependencias
cd backend
pip install -r requirements.txt

# 2. Vuelve a la raíz o levanta el servicio directamente
cd ..
python -m uvicorn backend.main:app --reload --port 8000
```

El servidor quedará encendido escuchando en `http://localhost:8000`. Puedes probar si funciona yendo a `http://localhost:8000/docs` en tu navegador, donde verás las rutas de la API.

### 4. Ejecutar el Frontend (Interfaz Visual)

Abre **otra** terminal y entra a la carpeta del frontend.
```bash
cd frontend
npm install
npm run dev
```

Se abrirá el sitio web localmente (usualmente en `http://localhost:5173`).


## 📡 ¿Cómo conectar tus propios sensores?

El backend tiene un endpoint expuesto para recibir peticiones por método POST. Tú puedes programar tus microcontroladores (ej: un ESP32 enviando HTTP POST vía WiFi) a la siguiente ruta:

**URL de endpoint (POST):**
`http://localhost:8000/data/` (Cambia localhost por la IP de tu servidor)

**Ejemplo de Petición JSON:**
```json
{
  "sensor_id": "sensor_esp32_01",
  "temperature_c": 22.5,
  "humidity_percent": 60.1,
  "ph_level": 7.2
}
```

La aplicación registrará esto en la base de datos y los gráficos en el Frontend se actualizarán automáticamente cada 10 segundos para mostrártelo en tiempo real.

## ✨ Características

- Visualización en tiempo real de Temperatura, Humedad y pH.
- Gráficos históricos interactivos.
- Alertas automáticas para valores fuera de rango (Anomalías).
- Clima local exterior y detección de desconexión del sensor integrado.
