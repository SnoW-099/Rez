import discord
from discord.ext import commands
from bank_system import BankSystem
from commands_manager import increment_command_count
import logging

logger = logging.getLogger(__name__)

# ID del owner del bot - cámbialo por tu ID de Discord
OWNER_ID = 465120268996444375  # Tu ID de Discord

def is_owner():
    """Check si el usuario es el owner del bot"""
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)

class OwnerCog(commands.Cog):
    """Comandos exclusivos para el owner del bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    @commands.command(name='addmoney', aliases=['addbal', 'givemoney'])
    @is_owner()
    async def add_money(self, ctx, member: discord.Member, amount: int):
        """[OWNER] Añade dinero a un usuario"""
        increment_command_count()
        
        if amount <= 0:
            await ctx.send("❌ La cantidad debe ser positiva.")
            return
        
        self.bank.add_money(member.id, amount)
        
        embed = discord.Embed(
            title="💰 Dinero Añadido",
            color=0x10b981
        )
        embed.add_field(name="Usuario", value=member.mention, inline=True)
        embed.add_field(name="Cantidad", value=f"+${amount:,}", inline=True)
        embed.add_field(name="Por", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} añadió ${amount} a {member}")

    @commands.command(name='removemoney', aliases=['removebal', 'takemoney'])
    @is_owner()
    async def remove_money(self, ctx, member: discord.Member, amount: int):
        """[OWNER] Quita dinero a un usuario"""
        increment_command_count()
        
        if amount <= 0:
            await ctx.send("❌ La cantidad debe ser positiva.")
            return
        
        actual_removed = self.bank.remove_money(member.id, amount)
        
        embed = discord.Embed(
            title="💸 Dinero Quitado",
            color=0xef4444
        )
        embed.add_field(name="Usuario", value=member.mention, inline=True)
        embed.add_field(name="Cantidad", value=f"-${actual_removed:,}", inline=True)
        embed.add_field(name="Por", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} quitó ${actual_removed} a {member}")

    @commands.command(name='setlevel')
    @is_owner()
    async def set_level(self, ctx, member: discord.Member, level: int):
        """[OWNER] Establece el nivel de un usuario"""
        increment_command_count()
        
        if level < 0:
            await ctx.send("❌ El nivel no puede ser negativo.")
            return
        
        # Calcular XP necesario para ese nivel
        xp_needed = self.bank.xp_for_level(level)
        
        self.bank.db.users.update_one(
            {'user_id': str(member.id)},
            {'$set': {'level': level, 'xp': xp_needed}}
        )
        
        embed = discord.Embed(
            title="⭐ Nivel Establecido",
            color=0x8b5cf6
        )
        embed.add_field(name="Usuario", value=member.mention, inline=True)
        embed.add_field(name="Nuevo Nivel", value=str(level), inline=True)
        embed.add_field(name="XP", value=f"{xp_needed:,}", inline=True)
        
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} estableció nivel {level} a {member}")

    @commands.command(name='resetuser')
    @is_owner()
    async def reset_user(self, ctx, member: discord.Member):
        """[OWNER] Reinicia todos los datos de un usuario"""
        increment_command_count()
        
        self.bank.db.users.delete_one({'user_id': str(member.id)})
        
        embed = discord.Embed(
            title="🔄 Usuario Reiniciado",
            description=f"Todos los datos de {member.mention} han sido eliminados.",
            color=0xf59e0b
        )
        
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} reinició a {member}")

    @commands.command(name='setbalance', aliases=['setbal'])
    @is_owner()
    async def set_balance(self, ctx, member: discord.Member, amount: int):
        """[OWNER] Establece el balance exacto de un usuario"""
        increment_command_count()
        
        self.bank.db.users.update_one(
            {'user_id': str(member.id)},
            {'$set': {'balance': amount}},
            upsert=True
        )
        
        embed = discord.Embed(
            title="💵 Balance Establecido",
            color=0x10b981
        )
        embed.add_field(name="Usuario", value=member.mention, inline=True)
        embed.add_field(name="Nuevo Balance", value=f"${amount:,}", inline=True)
        
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} estableció balance ${amount} a {member}")

    @commands.command(name='botstat')
    @is_owner()
    async def botstats(self, ctx):
        """[OWNER] Muestra estadísticas detalladas del bot"""
        increment_command_count()
        
        embed = discord.Embed(
            title="📊 Estadísticas del Bot",
            color=0x5865F2
        )
        embed.add_field(name="Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Usuarios", value=len(self.bot.users), inline=True)
        embed.add_field(name="Latencia", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        # Stats de MongoDB
        stats = self.bank.get_stats()
        embed.add_field(name="Usuarios en DB", value=stats.get('total_users', 0), inline=True)
        embed.add_field(name="Total Monedas", value=f"${stats.get('total_coins', 0):,}", inline=True)
        embed.add_field(name="XP Total", value=f"{stats.get('total_xp', 0):,}", inline=True)
        
        await ctx.send(embed=embed)

    # Error handler para comandos de owner
    @add_money.error
    @remove_money.error
    @set_level.error
    @reset_user.error
    @set_balance.error
    @botstats.error
    async def owner_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("❌ Solo el owner del bot puede usar este comando.")
        else:
            logger.error(f"Error en comando owner: {error}")

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
