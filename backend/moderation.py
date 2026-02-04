import discord
from discord.ext import commands
from bank_system import BankSystem
from commands_manager import increment_command_count

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        increment_command_count()
        self.bank.add_warning(member.id)
        warnings = self.bank.get_warnings(member.id)
        
        await ctx.send(f"⚠️ {member.mention} ha sido advertido. Advertencias totales: {warnings}")
        
        if warnings >= 3:
            try:
                await member.kick(reason="Demasiadas advertencias")
                await ctx.send(f"👢 {member.mention} ha sido expulsado por acumular 3 advertencias.")
                self.bank.reset_warnings(member.id)
            except discord.Forbidden:
                await ctx.send("No tengo permisos para expulsar a este usuario.")

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ No tienes permisos para usar este comando.")

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        increment_command_count()
        if amount <= 0 or amount > 100:
            await ctx.send("❌ Por favor, proporciona un número entre 1 y 100.")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 para incluir el comando
        await ctx.send(f"🗑️ Se eliminaron {len(deleted) - 1} mensajes.", delete_after=3)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ No tienes permisos para usar este comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Por favor, proporciona un número válido.")

    @commands.command(name='reset_warnings')
    @commands.has_permissions(administrator=True)
    async def reset_warnings(self, ctx, member: discord.Member):
        increment_command_count()
        self.bank.reset_warnings(member.id)
        await ctx.send(f"✅ Las advertencias de {member.mention} han sido reiniciadas.")

    @reset_warnings.error
    async def reset_warnings_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ No tienes permisos para usar este comando.")

# Función para añadir el cog al bot
async def setup(bot):
    await bot.add_cog(ModerationCog(bot))