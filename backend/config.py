import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Configuración de intents
intents = discord.Intents.default()
intents.message_content = True

# Creación del bot
bot = commands.Bot(command_prefix="$", intents=intents)

# Token del bot
TOKEN = os.getenv('DISCORD_TOKEN')