import asyncio
import threading
import discord
from discord.ext import commands
import sys
import os
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('RezBot')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_backend import config
from api_server import update_bot_status, run_api_server
from commands_manager import get_command_count
from database import database

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has logged in to Discord!')
    logger.info(f'Connected to {len(bot.guilds)} servers')
    logger.info(f'Serving {len(bot.users)} users')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers | !help"
        )
    )

    update_bot_status('online', len(bot.guilds), len(bot.users), 0)
    bot.loop.create_task(update_status_periodically())

async def update_status_periodically():
    while True:
        await asyncio.sleep(30)
        update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())
        
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(bot.guilds)} servers | !help"
            )
        )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏰ Wait {round(error.retry_after, 1)}s to use this command.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: `{error.param.name}`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument.")
    else:
        logger.error(f"Error in command {ctx.command}: {error}")

@bot.event
async def on_guild_join(guild):
    logger.info(f"New server: {guild.name} ({guild.member_count} members)")
    update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())

@bot.event
async def on_guild_remove(guild):
    logger.info(f"Left server: {guild.name}")
    update_bot_status('online', len(bot.guilds), len(bot.users), get_command_count())

async def load_extensions():
    extensions = ['commands', 'moderation', 'music', 'levels', 'games', 'giveaways', 'tickets', 'owner']
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ Extension loaded: {ext}")
        except Exception as e:
            logger.error(f"❌ Error loading {ext}: {e}")

async def setup_hook():
    await load_extensions()

async def main():
    bot.setup_hook = setup_hook
    
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()
    logger.info("API server started on port 3001")
    
    logger.info("=" * 50)
    logger.info("Starting Rez Bot v2.0 - Liquid Black Edition")
    logger.info("=" * 50)
    
    await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())