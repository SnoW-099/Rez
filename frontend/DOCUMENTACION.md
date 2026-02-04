# Rez Bot - Documentación del Dashboard Web

## Descripción

El dashboard web para Rez Bot es una aplicación React que proporciona una interfaz visual para monitorear y gestionar el estado del bot de Discord. La aplicación consume datos del servidor API del bot para mostrar información en tiempo real.

## Arquitectura

La aplicación está organizada en los siguientes componentes principales:

- `App.js`: Componente principal que gestiona la navegación y carga de datos
- `Navbar.js`: Barra de navegación para moverse entre vistas
- `BankDashboard.js`: Panel que muestra información del sistema bancario
- `BankCommands.js`: Información sobre comandos bancarios
- `api.js`: Funciones para interactuar con el servidor API
- `config.js`: Configuración de la aplicación

## Rutas

La aplicación incluye las siguientes vistas:

- `/` (Inicio): Vista principal con estadísticas generales y comandos básicos
- `/bank` (Sistema Bancario): Información detallada del sistema bancario
- `/commands` (Comandos): Lista completa de comandos disponibles
- `/stats` (Estadísticas): Estadísticas detalladas del bot

## API Endpoints Consumidos

La aplicación consume los siguientes endpoints del servidor API:

- `GET /api/status`: Estado actual del bot
- `GET /api/stats`: Estadísticas del bot (servidores, usuarios, etc.)
- `GET /api/commands`: Lista de comandos disponibles
- `GET /api/bank-data`: Datos del sistema bancario

## Estilos

La aplicación utiliza un diseño limpio con inspiración en el estilo de Apple, con:

- Colores suaves y modernos
- Tarjetas con sombras sutiles
- Transiciones suaves
- Diseño responsive para dispositivos móviles
- Indicadores visuales del estado del bot

## Configuración

La aplicación se puede configurar mediante variables de entorno en el archivo `.env`:

- `REACT_APP_API_URL`: URL del servidor API (por defecto: http://localhost:3001/api)
- `REACT_APP_BOT_CLIENT_ID`: ID del cliente del bot de Discord

## Despliegue

Para construir la aplicación para producción:

```bash
npm run build
```

La salida se generará en la carpeta `build/` y estará lista para ser servida por cualquier servidor web estático.

## Integración con el Backend

La aplicación está diseñada para funcionar junto con el servidor API del bot, que debe estar ejecutándose en el puerto 3001. La aplicación usa proxy para evitar problemas de CORS durante el desarrollo.