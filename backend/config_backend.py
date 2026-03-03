# config_backend.py - Archivo de configuración para el backend del bot

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """Configuración general del bot"""
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    BOT_NAME = os.getenv('BOT_NAME', 'Rez Bot')
    PREFIX = os.getenv('PREFIX', '!')
    
    # Configuración de la base de datos
    DB_PATH = os.getenv('DB_PATH', 'bank_data.json')
    
    # Configuración del servidor web (para la API)
    WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST', 'localhost')
    WEB_SERVER_PORT = int(os.getenv('WEB_SERVER_PORT', 3001))
    
    # Configuración de permisos
    ADMIN_ROLES = os.getenv('ADMIN_ROLES', '').split(',')
    MODERATOR_ROLES = os.getenv('MODERATOR_ROLES', '').split(',')
    
    # Configuración de comandos
    COOLDOWN_RATE = int(os.getenv('COOLDOWN_RATE', 1))
    COOLDOWN_PER = int(os.getenv('COOLDOWN_PER', 30))
    
    # Configuración de economía
    WORK_MIN_REWARD = int(os.getenv('WORK_MIN_REWARD', 50))
    WORK_MAX_REWARD = int(os.getenv('WORK_MAX_REWARD', 200))
    STARTING_BALANCE = int(os.getenv('STARTING_BALANCE', 1000))
    
    @classmethod
    def validate(cls):
        """Validar que la configuración sea correcta"""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN no está definido en las variables de entorno")
        return True

# Instancia global de la configuración
config = Config()