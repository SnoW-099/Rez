import discord
from discord.ext import commands
from datetime import timedelta
from bank_system import BankSystem
from commands_manager import increment_command_count
import logging

logger = logging.getLogger(__name__)

class ModerationCog(commands.Cog):
    """Comandos de moderación"""
    
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    # ============== WARN ==============

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "Sin razón especificada"):
        """Advierte a un usuario"""
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ No puedes advertir a alguien con un rol igual o superior.")
            return
        
        warnings = self.bank.add_warning(member.id)
        
        embed = discord.Embed(
            title="⚠️ Usuario Advertido",
            color=0xffa500
        )
        embed.add_field(name="Usuario", value=member.mention, inline=True)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="Advertencias", value=f"{warnings}/3", inline=True)
        embed.add_field(name="Razón", value=reason, inline=False)
        
        await ctx.send(embed=embed)
        
        # Auto-kick a las 3 advertencias
        if warnings >= 3:
            try:
                await member.kick(reason="3 advertencias acumuladas")
                await ctx.send(f"👢 **{member.display_name}** fue expulsado por acumular 3 advertencias.")
                self.bank.reset_warnings(member.id)
            except discord.Forbidden:
                await ctx.send("❌ No tengo permisos para expulsar.")

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Necesitas permiso para gestionar mensajes.")

    # ============== MUTE (Timeout) ==============

    @commands.command(name='mute', aliases=['timeout'])
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: str = "10m", *, reason: str = "Sin razón"):
        """Silencia a un usuario temporalmente (ej: !mute @user 10m)"""
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ No puedes silenciar a alguien con un rol igual o superior.")
            return
        
        # Parsear duración
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        unit = duration[-1].lower()
        
        if unit not in time_units:
            await ctx.send("❌ Formato inválido. Usa: `10s`, `5m`, `1h`, `1d`")
            return
        
        try:
            amount = int(duration[:-1])
        except ValueError:
            await ctx.send("❌ Cantidad inválida.")
            return
        
        seconds = amount * time_units[unit]
        if seconds > 2419200:  # 28 días máximo de Discord
            await ctx.send("❌ El máximo es 28 días.")
            return
        
        try:
            await member.timeout(timedelta(seconds=seconds), reason=reason)
            
            embed = discord.Embed(
                title="🔇 Usuario Silenciado",
                color=0xff6b6b
            )
            embed.add_field(name="Usuario", value=member.mention, inline=True)
            embed.add_field(name="Duración", value=duration, inline=True)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="Razón", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            logger.info(f"Mute: {member} por {duration} - {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ No tengo permisos para silenciar a este usuario.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Necesitas permiso para moderar miembros.")

    # ============== UNMUTE ==============

    @commands.command(name='unmute', aliases=['untimeout'])
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Quita el silencio a un usuario"""
        increment_command_count()
        
        try:
            await member.timeout(None)
            await ctx.send(f"🔊 **{member.display_name}** ya puede hablar de nuevo.")
        except discord.Forbidden:
            await ctx.send("❌ No tengo permisos para quitar el silencio.")

    # ============== BAN ==============

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "Sin razón"):
        """Banea a un usuario del servidor"""
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ No puedes banear a alguien con un rol igual o superior.")
            return
        
        try:
            # Enviar DM antes de banear
            try:
                await member.send(f"🚫 Has sido baneado de **{ctx.guild.name}**\nRazón: {reason}")
            except:
                pass
            
            await member.ban(reason=reason, delete_message_days=1)
            
            embed = discord.Embed(
                title="🔨 Usuario Baneado",
                color=0xff0000
            )
            embed.add_field(name="Usuario", value=f"{member} ({member.id})", inline=False)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="Razón", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            logger.info(f"Ban: {member} - {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ No tengo permisos para banear.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Necesitas permiso para banear miembros.")

    # ============== UNBAN ==============

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        """Desbanea a un usuario por su ID"""
        increment_command_count()
        
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"✅ **{user}** ha sido desbaneado.")
            logger.info(f"Unban: {user}")
        except discord.NotFound:
            await ctx.send("❌ Usuario no encontrado o no está baneado.")
        except discord.Forbidden:
            await ctx.send("❌ No tengo permisos para desbanear.")

    # ============== KICK ==============

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "Sin razón"):
        """Expulsa a un usuario del servidor"""
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ No puedes expulsar a alguien con un rol igual o superior.")
            return
        
        try:
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title="👢 Usuario Expulsado",
                color=0xffa500
            )
            embed.add_field(name="Usuario", value=f"{member}", inline=True)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="Razón", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send("❌ No tengo permisos para expulsar.")

    # ============== CLEAR ==============

    @commands.command(name='clear', aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Elimina mensajes del canal (1-100)"""
        increment_command_count()
        
        if amount < 1 or amount > 100:
            await ctx.send("❌ La cantidad debe estar entre 1 y 100.")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🗑️ Eliminados **{len(deleted) - 1}** mensajes.")
        await msg.delete(delay=3)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Necesitas permiso para gestionar mensajes.")

    # ============== SLOWMODE ==============

    @commands.command(name='slowmode', aliases=['slow'])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Establece el modo lento del canal (0 para desactivar)"""
        increment_command_count()
        
        if seconds < 0 or seconds > 21600:
            await ctx.send("❌ El slowmode debe estar entre 0 y 21600 segundos (6 horas).")
            return
        
        await ctx.channel.edit(slowmode_delay=seconds)
        
        if seconds == 0:
            await ctx.send("⚡ Slowmode **desactivado**.")
        else:
            await ctx.send(f"🐌 Slowmode establecido a **{seconds}** segundos.")

    # ============== RESET WARNINGS ==============

    @commands.command(name='reset_warnings', aliases=['clearwarns'])
    @commands.has_permissions(administrator=True)
    async def reset_warnings(self, ctx, member: discord.Member):
        """Reinicia las advertencias de un usuario"""
        increment_command_count()
        
        self.bank.reset_warnings(member.id)
        await ctx.send(f"✅ Advertencias de **{member.display_name}** reiniciadas.")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))