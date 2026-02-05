import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta
from bank_system import BankSystem
from commands_manager import increment_command_count

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        """Muestra el perfil de un usuario"""
        increment_command_count()
        if member is None:
            member = ctx.author
        
        user_data = self.bank.get_user_data(member.id)
        
        embed = discord.Embed(
            title=f"👤 Perfil de {member.display_name}",
            color=0x5865F2  # Discord blurple
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Economía
        embed.add_field(name="💰 Balance", value=f"${user_data['balance']:,}", inline=True)
        embed.add_field(name="📊 Total Ganado", value=f"${user_data.get('total_earned', 0):,}", inline=True)
        embed.add_field(name="💸 Total Gastado", value=f"${user_data.get('total_spent', 0):,}", inline=True)
        
        # XP y Nivel
        level = user_data.get('level', 0)
        xp = user_data.get('xp', 0)
        next_level_xp = self.bank.xp_for_level(level + 1)
        current_level_xp = self.bank.xp_for_level(level)
        progress = xp - current_level_xp
        needed = next_level_xp - current_level_xp
        
        embed.add_field(name="⭐ Nivel", value=str(level), inline=True)
        embed.add_field(name="✨ XP", value=f"{xp:,} / {next_level_xp:,}", inline=True)
        embed.add_field(name="💬 Mensajes", value=f"{user_data.get('messages', 0):,}", inline=True)
        
        # Moderación
        embed.add_field(name="⚠️ Advertencias", value=str(user_data['warnings']), inline=True)
        
        embed.set_footer(text=f"ID: {member.id}")
        await ctx.send(embed=embed)

    @commands.command(name='ranking')
    async def ranking(self, ctx):
        """Muestra el top 5 de usuarios más ricos"""
        increment_command_count()
        top_users = self.bank.get_top_users(5)
        
        embed = discord.Embed(title="🏆 Top 5 Usuarios Más Ricos", color=0xffd700)
        
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        for i, (user_id, data) in enumerate(top_users):
            try:
                user = await self.bot.fetch_user(int(user_id))
                username = user.name
            except:
                username = f"Usuario {user_id[:8]}..."
            
            embed.add_field(
                name=f"{medals[i]} {username}",
                value=f"${data['balance']:,}",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='work')
    async def work(self, ctx):
        """Trabaja para ganar dinero (cooldown: 3 minutos)"""
        increment_command_count()
        user_id = ctx.author.id
        
        # Verificar cooldown persistente
        remaining = self.bank.get_cooldown(user_id, 'work')
        if remaining > 0:
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            await ctx.send(f"⏰ Espera **{minutes}m {seconds}s** para volver a trabajar.")
            return
        
        # Trabajar y ganar dinero
        earnings = random.randint(50, 200)
        self.bank.add_money(user_id, earnings)
        self.bank.set_cooldown(user_id, 'work', 180)  # 3 minutos
        
        # Mensajes variados
        messages = [
            f"💼 Trabajaste en la oficina y ganaste **${earnings}**!",
            f"🏗️ Ayudaste en una construcción y te pagaron **${earnings}**!",
            f"🍕 Repartiste pizzas y ganaste **${earnings}** en propinas!",
            f"💻 Programaste unas horas y cobraste **${earnings}**!",
            f"🎨 Vendiste un dibujo por **${earnings}**!"
        ]
        
        await ctx.send(random.choice(messages))

    @commands.command(name='daily')
    async def daily(self, ctx):
        """Recoge tu recompensa diaria"""
        increment_command_count()
        user_id = ctx.author.id
        
        # Verificar cooldown de 24 horas
        remaining = self.bank.get_cooldown(user_id, 'daily')
        if remaining > 0:
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            await ctx.send(f"⏰ Ya recogiste tu daily. Vuelve en **{hours}h {minutes}m**.")
            return
        
        reward = random.randint(200, 500)
        self.bank.add_money(user_id, reward)
        self.bank.set_cooldown(user_id, 'daily', 86400)  # 24 horas
        
        await ctx.send(f"🎁 ¡Recogiste tu recompensa diaria de **${reward}**!")

    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        """Consulta tu saldo o el de otro usuario"""
        increment_command_count()
        if member is None:
            member = ctx.author
        
        user_data = self.bank.get_user_data(member.id)
        await ctx.send(f"💰 **{member.display_name}** tiene **${user_data['balance']:,}**")

    @commands.command(name='transfer', aliases=['pay', 'give'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfiere dinero a otro usuario"""
        increment_command_count()
        
        if member.id == ctx.author.id:
            await ctx.send("❌ No puedes transferirte dinero a ti mismo.")
            return
        
        if amount <= 0:
            await ctx.send("❌ La cantidad debe ser mayor a 0.")
            return
        
        sender_data = self.bank.get_user_data(ctx.author.id)
        if sender_data['balance'] < amount:
            await ctx.send("❌ No tienes suficiente dinero.")
            return
        
        self.bank.remove_money(ctx.author.id, amount)
        self.bank.add_money(member.id, amount)
        
        await ctx.send(f"✅ Transferiste **${amount:,}** a **{member.display_name}**")

    @commands.command(name='rob')
    async def rob(self, ctx, member: discord.Member):
        """Intenta robar dinero a otro usuario (50% de éxito)"""
        increment_command_count()
        
        if member.id == ctx.author.id:
            await ctx.send("❌ No puedes robarte a ti mismo.")
            return
        
        # Cooldown de robo
        remaining = self.bank.get_cooldown(ctx.author.id, 'rob')
        if remaining > 0:
            await ctx.send(f"⏰ Espera **{int(remaining)}s** para intentar robar de nuevo.")
            return
        
        self.bank.set_cooldown(ctx.author.id, 'rob', 120)  # 2 minutos
        
        victim_data = self.bank.get_user_data(member.id)
        if victim_data['balance'] < 100:
            await ctx.send(f"💸 **{member.display_name}** no tiene suficiente dinero para robar.")
            return
        
        if random.random() > 0.5:  # 50% éxito
            stolen = min(random.randint(50, 200), victim_data['balance'])
            self.bank.add_money(ctx.author.id, stolen)
            self.bank.remove_money(member.id, stolen)
            await ctx.send(f"💰 ¡Robo exitoso! Robaste **${stolen}** a **{member.display_name}**")
        else:
            penalty = random.randint(50, 150)
            actual = self.bank.remove_money(ctx.author.id, penalty)
            await ctx.send(f"👮 ¡Te atraparon! Pagaste una multa de **${actual}**")

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Verifica la latencia del bot"""
        increment_command_count()
        latency = round(self.bot.latency * 1000)
        
        if latency < 100:
            status = "🟢 Excelente"
        elif latency < 200:
            status = "🟡 Buena"
        else:
            status = "🔴 Alta"
        
        await ctx.send(f"🏓 Pong! **{latency}ms** ({status})")

    @commands.command(name='help')
    async def show_help(self, ctx):
        """Muestra todos los comandos disponibles"""
        increment_command_count()
        
        embed = discord.Embed(
            title="🤖 Rez Bot - Comandos",
            description="Prefijo: `!`",
            color=0x5865F2
        )
        
        # Economía
        economy = """
        `!profile` - Tu perfil completo
        `!balance` - Consulta tu saldo
        `!work` - Trabaja (cooldown: 3min)
        `!daily` - Recompensa diaria
        `!transfer @user cantidad` - Transferir
        `!rob @user` - Robar (50% éxito)
        `!ranking` - Top 5 más ricos
        """
        embed.add_field(name="💰 Economía", value=economy, inline=False)
        
        # XP
        xp = """
        `!level` - Ver tu nivel
        `!leaderboard` - Top 10 XP
        """
        embed.add_field(name="⭐ Niveles", value=xp, inline=False)
        
        # Moderación
        mod = """
        `!warn @user` - Advertir
        `!mute @user [tiempo]` - Silenciar
        `!ban @user` - Banear
        `!clear cantidad` - Borrar mensajes
        """
        embed.add_field(name="🛡️ Moderación", value=mod, inline=False)
        
        embed.set_footer(text="Rez Bot v2.0 | Liquid Black Edition")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandsCog(bot))