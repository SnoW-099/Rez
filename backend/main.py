# main.py - Punto de entrada principal del bot de Discord

import asyncio
import threading
import discord
from discord.ext import commands
import sys
import os
from datetime import datetime

# Añadir el directorio backend al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_backend import config
from api_server import update_bot_status, run_api_server
from commands_manager import get_command_count

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Inicializar el bot
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión en Discord!')
    print(f'Conectado a {len(bot.guilds)} servidores')
    print(f'Sirviendo a {len(bot.users)} usuarios')

    # Actualizar el estado del bot en la API
    update_bot_status('online', len(bot.guilds), len(bot.users), 0)

    # Actualizar periodicamente el estado
    bot.loop.create_task(update_status_periodically())

async def update_status_periodically():
    """Actualizar el estado del bot periódicamente"""
    while True:
        await asyncio.sleep(30)  # Actualizar cada 30 segundos
        update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())

@bot.event
async def on_command_completion(ctx):
    """Evento cuando se completa un comando"""
    # El conteo de comandos se maneja en cada comando individual
    pass

# Cargar extensiones
async def load_extensions():
    await bot.load_extension('commands')
    await bot.load_extension('moderation')
    await bot.load_extension('music')

async def setup_hook():
    await load_extensions()

async def main():
    # Configurar el hook de setup
    bot.setup_hook = setup_hook

    # Iniciar el servidor API en un hilo separado
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()

    # Iniciar el bot
    async with bot:
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        config.validate()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot detenido manualmente")
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")
        sys.exit(1)