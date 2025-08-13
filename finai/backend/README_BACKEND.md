# Backend Django (FinAI)

## Quickstart
```
# Crear venv (si está disponible) o instalar con --break-system-packages
python3 -m venv .venv || true
source .venv/bin/activate || true
pip install -r requirements.txt --break-system-packages
cp .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Variables de entorno clave:
- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `GOOGLE_APPLICATION_CREDENTIALS` o `FIREBASE_CREDENTIALS_JSON`

## Endpoints
- `GET /api/health` OK sin auth
- `GET /api/colcap/tickers` lista de tickers (auth requerida)
- `GET /api/colcap/scan?period=1y&interval=1d` clasificación buy/sell (auth requerida)
- `GET /api/colcap/indicators/<symbol>?period=1y&interval=1d` snapshot indicadores (auth requerida)
- `GET /api/colcap/me/preferences` preferencias de usuario (Firestore)
- `POST /api/colcap/me/preferences/save` { preferences } guarda preferencias

Header de autenticación: `Authorization: Bearer <ID_TOKEN_FIREBASE>`

## Modulos
- `market/services/yf_client.py` descarga con cache TTL
- `market/services/indicators.py` RSI, MACD, VWAP, EMAs 25/50/100/200/1000
- `market/services/classifier.py` reglas parametrizables
- `market/auth` verificación Firebase
- `market/services/db.py` acceso a Firestore para preferencias