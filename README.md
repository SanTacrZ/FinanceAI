# FinAI Monorepo (Backend Django + Frontend React)

FinAI es una plataforma de analítica para el mercado colombiano (COLCAP) que integra:
- Backend en Django (API REST) con autenticación mediante Firebase (incl. Google Sign-In).
- Frontend en React (Vite) con login de Google y vistas de oportunidades de compra y potencial caída.
- Recolección de datos desde Yahoo Finance y cálculo de indicadores técnicos (RSI, MACD, VWAP, EMA 25/50/100/200/1000).

## Estructura del Proyecto

```
finai/
├─ backend/
│  ├─ backend/               # Proyecto Django
│  ├─ market/                # App de mercado (COLCAP)
│  │  ├─ services/           # Yahoo, indicadores, clasificación, caché
│  │  ├─ data/               # Configuración de tickers COLCAP
│  │  └─ auth/               # Integración Firebase (server)
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend/
│  ├─ src/
│  │  ├─ pages/              # Login / Dashboard
│  │  ├─ components/         # UI de tarjetas de señales
│  │  └─ firebase.js         # Config cliente Firebase
│  ├─ index.html
│  ├─ package.json
│  └─ .env.example
└─ README.md
```

## Backend (Django API)
- Endpoints principales:
  - `GET /api/health` estado del servicio.
  - `GET /api/colcap/tickers` lista de tickers soportados (con mapeo Yahoo).
  - `GET /api/colcap/scan?period=1y&interval=1d` clasifica acciones/índices en:
    - `buy_opportunities` (oportunidad de compra)
    - `sell_risks` (potencial caída)
  - `GET /api/colcap/indicators/<symbol>?period=1y&interval=1d` indicadores calculados.
- Autenticación: verificación de ID Token de Firebase usando `Authorization: Bearer <ID_TOKEN>`.
- Cálculo de indicadores: RSI, MACD, VWAP y EMAs (25/50/100/200/1000).
- Caché en memoria con TTL para reducir llamadas a Yahoo Finance.

### Requisitos e instalación (recomendado en venv)
```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Establece variables en .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Variables de entorno relevantes (`backend/.env.example`):
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (0/1)
- `DJANGO_ALLOWED_HOSTS` (separado por coma)
- `GOOGLE_APPLICATION_CREDENTIALS` (ruta al JSON de service account) o `FIREBASE_CREDENTIALS_JSON` (contenido JSON inline)
- `CORS_ALLOWED_ORIGINS` (ej: http://localhost:5173)

## Frontend (React + Vite)
```
cd frontend
npm i
cp .env.example .env
npm run dev
```
Variables (`frontend/.env.example`):
- `VITE_API_BASE_URL` (ej: http://localhost:8000)
- `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_AUTH_DOMAIN`, `VITE_FIREBASE_PROJECT_ID`, `VITE_FIREBASE_APP_ID`, etc.

### Flujo de autenticación
1. El usuario inicia sesión con Google en el frontend (Firebase Auth).
2. El frontend obtiene el ID Token de Firebase y lo envía al backend en el header `Authorization`.
3. El backend valida el token con Firebase Admin y autoriza el acceso.

## Clasificación (reglas iniciales)
- Compra (buy_opportunity) cuando:
  - Precio > EMA50 y > EMA200
  - RSI en [50, 65]
  - MACD hist > 0 y cruce reciente al alza
  - Precio > VWAP
- Venta (sell_risk) cuando:
  - Precio < EMA50 y < EMA200
  - RSI < 45
  - MACD hist < 0 y cruce reciente a la baja
  - Precio < VWAP

Estas reglas son configurables y mejorables en `market/services/classifier.py`.

## Roadmap breve
- Guardar preferencias del usuario en Firestore (watchlists, portafolios).
- Jobs periódicos para precalcular señales y mejorar latencia.
- Backtesting y ranking por score de calidad de señal.
- UI avanzada con gráficos y filtros.

## Licencia
Este proyecto es de uso interno/educativo. Ajusta según tus necesidades.