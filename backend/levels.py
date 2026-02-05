import discord
from discord.ext import commands
import random
from bank_system import BankSystem
from commands_manager import increment_command_count

class LevelsCog(commands.Cog):
    """Sistema de niveles y XP"""
    
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()
        self.xp_per_message = (15, 25)  # Min, Max XP por mensaje
        self.xp_cooldown = 60  # Segundos entre ganancia de XP

    @commands.Cog.listener()
    async def on_message(self, message):
        """Dar XP por cada mensaje (con cooldown)"""
        # Ignorar bots y comandos
        if message.author.bot:
            return
        if message.content.startswith('!'):
            return
        
        user_id = message.author.id
        
        # Verificar cooldown de XP
        if not self.bank.can_gain_xp(user_id, self.xp_cooldown):
            return
        
        # Dar XP aleatorio
        xp_gained = random.randint(*self.xp_per_message)
        leveled_up, new_level = self.bank.add_xp(user_id, xp_gained)
        
        # Notificar si subió de nivel
        if leveled_up:
            embed = discord.Embed(
                title="🎉 ¡Subiste de Nivel!",
                description=f"**{message.author.display_name}** alcanzó el nivel **{new_level}**!",
                color=0xffd700
            )
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
            
            # Bonus por subir de nivel
            bonus = new_level * 50
            self.bank.add_money(user_id, bonus)
            embed.add_field(name="🎁 Bonus", value=f"+${bonus}", inline=False)
            
            await message.channel.send(embed=embed)

    @commands.command(name='level', aliases=['lvl', 'nivel'])
    async def level(self, ctx, member: discord.Member = None):
        """Ver tu nivel o el de otro usuario"""
        increment_command_count()
        
        if member is None:
            member = ctx.author
        
        user_data = self.bank.get_user_data(member.id)
        level = user_data.get('level', 0)
        xp = user_data.get('xp', 0)
        messages = user_data.get('messages', 0)
        
        # Calcular progreso
        current_level_xp = self.bank.xp_for_level(level)
        next_level_xp = self.bank.xp_for_level(level + 1)
        progress = xp - current_level_xp
        needed = next_level_xp - current_level_xp
        percentage = int((progress / needed) * 100) if needed > 0 else 100
        
        # Barra de progreso visual
        filled = int(percentage / 10)
        bar = "▓" * filled + "░" * (10 - filled)
        
        embed = discord.Embed(
            title=f"⭐ Nivel de {member.display_name}",
            color=0x5865F2
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        embed.add_field(name="Nivel", value=f"**{level}**", inline=True)
        embed.add_field(name="XP Total", value=f"**{xp:,}**", inline=True)
        embed.add_field(name="Mensajes", value=f"**{messages:,}**", inline=True)
        
        embed.add_field(
            name=f"Progreso al nivel {level + 1}",
            value=f"`{bar}` {percentage}%\n{progress:,} / {needed:,} XP",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='leaderboard', aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        """Ver el top 10 de XP"""
        increment_command_count()
        
        top_users = self.bank.get_xp_leaderboard(10)
        
        embed = discord.Embed(
            title="🏆 Leaderboard de XP",
            color=0xffd700
        )
        
        medals = ["🥇", "🥈", "🥉"] + [f"`{i}.`" for i in range(4, 11)]
        
        description = ""
        for i, user_data in enumerate(top_users):
            try:
                user = await self.bot.fetch_user(int(user_data['user_id']))
                username = user.name
            except:
                username = f"Usuario {user_data['user_id'][:8]}..."
            
            level = user_data.get('level', 0)
            xp = user_data.get('xp', 0)
            
            description += f"{medals[i]} **{username}** - Nivel {level} ({xp:,} XP)\n"
        
        embed.description = description or "No hay usuarios todavía."
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LevelsCog(bot))
