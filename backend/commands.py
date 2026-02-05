import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime, timedelta
from bank_system import BankSystem
from commands_manager import increment_command_count, get_command_count

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()
        self.work_cooldown = {}

    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        increment_command_count()
        if member is None:
            member = ctx.author
        
        user_data = self.bank.get_user_data(member.id)
        embed = discord.Embed(title=f"Perfil de {member.display_name}", color=0x00ff00)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Dinero", value=f"${user_data['balance']}", inline=False)
        embed.add_field(name="Advertencias", value=user_data['warnings'], inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='ranking')
    async def ranking(self, ctx):
        increment_command_count()
        top_users = self.bank.get_top_users(5)
        embed = discord.Embed(title="🏆 Top 5 Usuarios", color=0xffd700)
        
        for i, (user_id, data) in enumerate(top_users, start=1):
            user = await self.bot.fetch_user(user_id)
            username = user.name if user else f"Usuario Desconocido ({user_id})"
            embed.add_field(name=f"{i}. {username}", value=f"${data['balance']}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='work')
    async def work(self, ctx):
        increment_command_count()
        user_id = ctx.author.id
        
        if user_id in self.work_cooldown:
            remaining_time = self.work_cooldown[user_id] - datetime.now()
            if remaining_time.total_seconds() > 0:
                await ctx.send(f"⏰ Espera {int(remaining_time.total_seconds())} segundos para volver a trabajar.")
                return
        
        earnings = random.randint(50, 200)
        self.bank.add_money(user_id, earnings)
        self.work_cooldown[user_id] = datetime.now() + timedelta(minutes=3)
        
        await ctx.send(f"💼 Trabajaste duro y ganaste ${earnings}!")

    @commands.command(name='balance')
    async def balance(self, ctx, member: discord.Member = None):
        increment_command_count()
        if member is None:
            member = ctx.author
        
        user_data = self.bank.get_user_data(member.id)
        await ctx.send(f"💰 {member.display_name} tiene ${user_data['balance']}")

    @commands.command(name='transfer', aliases=['pay'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        increment_command_count()
        if amount <= 0:
            await ctx.send("❌ La cantidad debe ser mayor a 0.")
            return
        
        sender_data = self.bank.get_user_data(ctx.author.id)
        if sender_data['balance'] < amount:
            await ctx.send("❌ No tienes suficiente dinero para transferir.")
            return
        
        self.bank.remove_money(ctx.author.id, amount)
        self.bank.add_money(member.id, amount)
        
        await ctx.send(f"✅ Transferiste ${amount} a {member.display_name}")

    @commands.command(name='rob')
    async def rob(self, ctx, member: discord.Member):
        increment_command_count()
        if member.id == ctx.author.id:
            await ctx.send("❌ No puedes robarte a ti mismo.")
            return
        
        success_rate = random.random()
        if success_rate > 0.5:  # 50% de éxito
            victim_data = self.bank.get_user_data(member.id)
            if victim_data['balance'] < 100:
                await ctx.send(f"💸 {member.display_name} no tiene suficiente dinero para robar.")
                return
            
            stolen_amount = min(random.randint(50, 200), victim_data['balance'])
            self.bank.add_money(ctx.author.id, stolen_amount)
            self.bank.remove_money(member.id, stolen_amount)
            
            await ctx.send(f"💰 ¡Robo exitoso! Robaste ${stolen_amount} a {member.display_name}")
        else:
            penalty = random.randint(50, 150)
            author_data = self.bank.get_user_data(ctx.author.id)
            actual_penalty = min(penalty, author_data['balance'])
            
            self.bank.remove_money(ctx.author.id, actual_penalty)
            await ctx.send(f"👮‍♂️ ¡Fallaste en el robo! Pagaste una multa de ${actual_penalty}")

    @commands.command(name='ping')
    async def ping(self, ctx):
        increment_command_count()
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! 🏓 Latencia: {latency}ms")

    @commands.command(name='help')
    async def show_help(self, ctx):
        increment_command_count()
        embed = discord.Embed(title="🤖 Rez Bot - Comandos Disponibles", color=0x3498db)
        
        commands_list = [
            ("!profile", "Muestra tu perfil de usuario"),
            ("!ranking", "Muestra el top 5 de usuarios más ricos"),
            ("!work", "Trabaja para ganar dinero (cooldown: 3 minutos)"),
            ("!balance", "Consulta tu saldo"),
            ("!transfer @usuario cantidad", "Transfiere dinero a otro usuario"),
            ("!rob @usuario", "Intenta robarle dinero a otro usuario"),
            ("!ping", "Verifica la latencia del bot"),
            ("!warn @usuario", "Advierte a un usuario (solo admins/mods)"),
            ("!clear cantidad", "Elimina mensajes (solo admins/mods)")
        ]
        
        for cmd, desc in commands_list:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        await ctx.send(embed=embed)

# Función para añadir el cog al bot
async def setup(bot):
    await bot.add_cog(CommandsCog(bot))