# Rez 🤖 | Security & Economy System

Rez es un bot de Discord de alto rendimiento diseñado para equilibrar la gestión de comunidad con un sistema económico competitivo. Enfocado en la **seriedad, eficiencia y seguridad**.

> 🛡️ **Estado del Proyecto**: Beta Activa. Rez ya cuenta con persistencia de datos y módulos de administración independientes.

## 🛠️ Arquitectura del Proyecto

El bot utiliza una estructura modular para garantizar la estabilidad y facilitar el mantenimiento:

* `main.py`: Núcleo de ejecución y orquestador de módulos.
* `config.py`: Gestión de Intents y configuración de API.
* `moderation.py`: Sistema de seguridad, filtros y control de usuarios.
* `commands.py`: Lógica económica y utilidades.
* `bank_system.py`: Motor de base de datos JSON y persistencia.

## ✨ Características Principales

### 🛡️ Módulo de Seguridad (Security)
* **Sistema de Warns**: Registro persistente de amonestaciones con expulsión automática tras 3 avisos.
* **Anti-Spam de Invitaciones**: Filtro inteligente que bloquea enlaces de otros servidores (bypass para administradores).
* **Limpieza de Logs**: Comandos rápidos para mantenimiento de canales.

### 💰 Sistema Económico (Economy)
* **Persistencia Total**: Los saldos y registros se guardan en tiempo real.
* **Interacción Social**: Comandos de transferencia (donar), azar (trabajar/robar) y competitividad.
* **Ranking Global**: Visualización de los usuarios más influyentes del servidor mediante Embeds.

## 📜 Lista de Comandos

| Comando | Categoría | Descripción |
| :--- | :--- | :--- |
| `$perfil` | Utilidad | Muestra la ficha técnica, saldo y historial de seguridad. |
| `$ranking` | Economía | Top 5 de usuarios con mayor liquidez. |
| `$warn` | Seguridad | Añade un aviso a un usuario (Admin). |
| `$limpiar` | Moderación | Borrado masivo de mensajes. |
| `$trabajar` | Economía | Genera ingresos aleatorios (Cooldown de 3 min). |

## 🌐 Despliegue y Pruebas

Actualmente, Rez se encuentra en fase de **Beta Privada**. 

1. Clona el repositorio.
2. Crea un archivo `.env` con tu `DISCORD_TOKEN`.
3. Instala las dependencias: `pip install discord.py python-dotenv`.
4. Ejecuta `main.py` para iniciar el sistema.

---
Desarrollado con 💻 por **Snow099** ⭐
