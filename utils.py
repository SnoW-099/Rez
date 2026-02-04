from discord.ext import commands

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"¡Cálmate! Inténtalo de nuevo en {round(error.retry_after, 2)} segundos.")