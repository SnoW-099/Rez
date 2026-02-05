# main.py - Punto de entrada principal del bot de Discord

import asyncio
import threading
import discord
from discord.ext import commands
import sys
import os
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('RezBot')

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
bot.remove_command('help')  # Eliminar el comando help por defecto para usar el personalizado

@bot.event
async def on_ready():
    logger.info(f'{bot.user} ha iniciado sesión en Discord!')
    logger.info(f'Conectado a {len(bot.guilds)} servidores')
    logger.info(f'Sirviendo a {len(bot.users)} usuarios')
    
    # Establecer presencia del bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servidores | !help"
        )
    )

    # Actualizar el estado del bot en la API
    update_bot_status('online', len(bot.guilds), len(bot.users), 0)

    # Actualizar periodicamente el estado
    bot.loop.create_task(update_status_periodically())

async def update_status_periodically():
    """Actualizar el estado del bot periódicamente"""
    while True:
        await asyncio.sleep(30)  # Actualizar cada 30 segundos
        update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())
        
        # Actualizar presencia
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(bot.guilds)} servidores | !help"
            )
        )

@bot.event
async def on_command_error(ctx, error):
    """Manejo global de errores de comandos"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignorar comandos no encontrados
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏰ Espera {round(error.retry_after, 1)} segundos para usar este comando de nuevo.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Falta un argumento: `{error.param.name}`")
    else:
        logger.error(f"Error en comando: {error}")

@bot.event
async def on_command_completion(ctx):
    """Evento cuando se completa un comando"""
    logger.debug(f"Comando ejecutado: {ctx.command.name} por {ctx.author}")

# Cargar extensiones
async def load_extensions():
    await bot.load_extension('commands')
    await bot.load_extension('moderation')
    await bot.load_extension('music')
    logger.info("Extensiones cargadas correctamente")

async def setup_hook():
    await load_extensions()

async def main():
    # Configurar el hook de setup
    bot.setup_hook = setup_hook

    # Iniciar el servidor API en un hilo separado
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()
    logger.info("Servidor API iniciado en hilo separado")

    # Iniciar el bot
    async with bot:
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        config.validate()
        logger.info("Iniciando Rez Bot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot detenido manualmente")
    except Exception as e:
        logger.error(f"Error al iniciar el bot: {e}")
        sys.exit(1)