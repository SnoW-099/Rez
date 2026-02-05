import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta
from commands_manager import increment_command_count
import logging

logger = logging.getLogger(__name__)

class GiveawayCog(commands.Cog):
    """Sistema de sorteos"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}

    @commands.command(name='giveaway', aliases=['sorteo', 'gstart'])
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx, duration: str, *, prize: str):
        """Crea un sorteo. Uso: !giveaway 1h Premio Especial"""
        increment_command_count()
        
        # Parsear duración
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        unit = duration[-1].lower()
        
        if unit not in time_units:
            await ctx.send("❌ Formato inválido. Usa: `1m`, `1h`, `1d`")
            return
        
        try:
            amount = int(duration[:-1])
        except ValueError:
            await ctx.send("❌ Duración inválida.")
            return
        
        seconds = amount * time_units[unit]
        if seconds > 604800:  # 7 días máximo
            await ctx.send("❌ Máximo 7 días.")
            return
        
        end_time = datetime.utcnow() + timedelta(seconds=seconds)
        
        embed = discord.Embed(
            title="🎉 SORTEO 🎉",
            description=f"**Premio:** {prize}\n\nReacciona con 🎁 para participar!",
            color=0x10b981
        )
        embed.add_field(name="Termina en", value=f"<t:{int(end_time.timestamp())}:R>", inline=True)
        embed.add_field(name="Host", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎁")
        
        self.active_giveaways[msg.id] = {
            'channel_id': ctx.channel.id,
            'prize': prize,
            'host': ctx.author.id,
            'end_time': end_time,
            'message_id': msg.id
        }
        
        # Esperar y terminar sorteo
        await asyncio.sleep(seconds)
        await self.end_giveaway(msg.id)

    async def end_giveaway(self, message_id):
        """Termina un sorteo y elige ganador"""
        if message_id not in self.active_giveaways:
            return
        
        giveaway = self.active_giveaways.pop(message_id)
        
        try:
            channel = self.bot.get_channel(giveaway['channel_id'])
            message = await channel.fetch_message(message_id)
            
            # Obtener participantes
            users = []
            for reaction in message.reactions:
                if str(reaction.emoji) == "🎁":
                    async for user in reaction.users():
                        if not user.bot:
                            users.append(user)
            
            if not users:
                embed = discord.Embed(
                    title="🎉 Sorteo Terminado",
                    description="No hubo participantes 😢",
                    color=0xef4444
                )
                await channel.send(embed=embed)
                return
            
            winner = random.choice(users)
            
            embed = discord.Embed(
                title="🎉 ¡Tenemos un Ganador!",
                description=f"**Premio:** {giveaway['prize']}\n\n🏆 **Ganador:** {winner.mention}",
                color=0x10b981
            )
            embed.set_thumbnail(url=winner.avatar.url if winner.avatar else winner.default_avatar.url)
            
            await channel.send(f"🎊 Felicidades {winner.mention}!", embed=embed)
            logger.info(f"Sorteo terminado: {winner} ganó '{giveaway['prize']}'")
            
        except Exception as e:
            logger.error(f"Error terminando sorteo: {e}")

    @commands.command(name='gend', aliases=['endgiveaway'])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_end(self, ctx, message_id: int = None):
        """Termina un sorteo manualmente"""
        increment_command_count()
        
        if message_id is None:
            # Buscar el último sorteo activo
            if not self.active_giveaways:
                await ctx.send("❌ No hay sorteos activos.")
                return
            message_id = list(self.active_giveaways.keys())[-1]
        
        if message_id not in self.active_giveaways:
            await ctx.send("❌ Sorteo no encontrado.")
            return
        
        await self.end_giveaway(message_id)
        await ctx.send("✅ Sorteo terminado!")

    @commands.command(name='greroll', aliases=['reroll'])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_reroll(self, ctx, message_id: int):
        """Vuelve a sortear un ganador"""
        increment_command_count()
        
        try:
            message = await ctx.channel.fetch_message(message_id)
            
            users = []
            for reaction in message.reactions:
                if str(reaction.emoji) == "🎁":
                    async for user in reaction.users():
                        if not user.bot:
                            users.append(user)
            
            if not users:
                await ctx.send("❌ No hay participantes.")
                return
            
            winner = random.choice(users)
            await ctx.send(f"🎊 ¡Nuevo ganador: {winner.mention}!")
            
        except discord.NotFound:
            await ctx.send("❌ Mensaje no encontrado.")

async def setup(bot):
    await bot.add_cog(GiveawayCog(bot))
