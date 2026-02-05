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
from database import database

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Inicializar el bot
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)
bot.remove_command('help')  # Eliminar el comando help por defecto

@bot.event
async def on_ready():
    logger.info(f'{bot.user} ha iniciado sesión en Discord!')
    logger.info(f'Conectado a {len(bot.guilds)} servidores')
    logger.info(f'Sirviendo a {len(bot.users)} usuarios')
    
    # Verificar conexión a MongoDB
    try:
        database.connect()
        logger.info("Conexión a MongoDB verificada")
    except Exception as e:
        logger.error(f"Error conectando a MongoDB: {e}")
    
    # Establecer presencia del bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servidores | !help"
        )
    )

    # Actualizar el estado del bot en la API
    update_bot_status('online', len(bot.guilds), len(bot.users), 0)

    # Actualizar periódicamente el estado
    bot.loop.create_task(update_status_periodically())

async def update_status_periodically():
    """Actualizar el estado del bot periódicamente"""
    while True:
        await asyncio.sleep(30)
        update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())
        
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
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏰ Espera {round(error.retry_after, 1)}s para usar este comando.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Falta un argumento: `{error.param.name}`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argumento inválido.")
    else:
        logger.error(f"Error en comando {ctx.command}: {error}")

@bot.event
async def on_guild_join(guild):
    """Cuando el bot se une a un servidor"""
    logger.info(f"Nuevo servidor: {guild.name} ({guild.member_count} miembros)")
    update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())

@bot.event
async def on_guild_remove(guild):
    """Cuando el bot es removido de un servidor"""
    logger.info(f"Servidor removido: {guild.name}")
    update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())

# Cargar extensiones
async def load_extensions():
    extensions = ['commands', 'moderation', 'music', 'levels']
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ Extensión cargada: {ext}")
        except Exception as e:
            logger.error(f"❌ Error cargando {ext}: {e}")

async def setup_hook():
    await load_extensions()

async def main():
    bot.setup_hook = setup_hook

    # Iniciar el servidor API en un hilo separado
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()
    logger.info("Servidor API iniciado en puerto 3001")

    # Iniciar el bot
    async with bot:
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        config.validate()
        logger.info("=" * 50)
        logger.info("Iniciando Rez Bot v2.0 - Liquid Black Edition")
        logger.info("=" * 50)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot detenido manualmente")
    except Exception as e:
        logger.error(f"Error al iniciar el bot: {e}")
        sys.exit(1)