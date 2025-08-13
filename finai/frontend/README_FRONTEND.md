# Frontend React (Vite)

## Quickstart
```
npm i
cp .env.example .env
# Llena tus credenciales de Firebase y la URL del backend
npm run dev
```

## Rutas
- `/login` Autenticación con Google (Firebase)
- `/` Dashboard con 2 columnas: oportunidades de compra y potencial caída (consume `/api/colcap/scan`)

El frontend envía el token de Firebase en el header `Authorization: Bearer <id_token>` a todas las llamadas Axios.