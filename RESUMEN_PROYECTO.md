# Rez Bot - Dashboard Web Completo

## Resumen del Proyecto

Has creado una aplicación web completa para monitorear y gestionar tu bot de Discord Rez. El proyecto incluye:

### Backend (Ya existente)
- Bot de Discord con sistema bancario/economía
- Sistema de comandos: $balance, $trabajar, $robar, $donar, $ranking, $perfil
- Servidor API en Flask que expone endpoints para la web

### Frontend (Nuevo)
- Aplicación React con diseño estilo Apple
- Dashboard principal con estadísticas del bot
- Sección dedicada al sistema bancario con datos en tiempo real
- Vista de comandos disponibles
- Navegación entre diferentes secciones
- Diseño responsive para dispositivos móviles

## Características Destacadas

1. **Dashboard Principal**: Muestra estado del bot, servidores, usuarios y comandos usados
2. **Sistema Bancario**: Visualización de datos del sistema económico del bot
3. **Comandos**: Lista completa de comandos disponibles
4. **Estadísticas**: Métricas detalladas del bot
5. **Navegación**: Interfaz intuitiva con menú de navegación

## Tecnologías Utilizadas

- **Frontend**: React, JavaScript, CSS
- **Backend**: Python, Flask, Discord.py
- **API**: Endpoints REST para comunicación
- **Estilos**: Diseño tipo Apple con colores suaves y tarjetas

## Cómo Ejecutar

1. Asegúrate de tener Python y Node.js instalados
2. Instala las dependencias del backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```
3. Instala las dependencias del frontend:
   ```
   cd frontend
   npm install
   ```
4. Crea un archivo `.env` en el directorio backend con tu token de Discord
5. Ejecuta el script de inicio:
   ```
   start_app.bat
   ```

## Personalización

Puedes personalizar la aplicación modificando:

- Componentes React en `frontend/src/components/`
- Estilos en `frontend/src/App.css`
- Configuración en `frontend/src/config.js`
- Endpoints API en `backend/api_server.py`

## Próximos Pasos Sugeridos

1. Agregar autenticación para proteger el dashboard
2. Implementar controles administrativos para moderar el bot
3. Añadir gráficos para visualizar tendencias
4. Incorporar sistema de logs
5. Agregar capacidad para enviar comandos al bot desde la web

¡Tu dashboard web para Rez Bot está listo para usar!