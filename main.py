import random

import discord
from discord.ext import commands

from bank_system import banco, cargar_banco, guardar_banco
from config import TOKEN, bot

cargar_banco()
bot.remove_command("help")


@bot.command()
async def balance(ctx):
    usuario_id = str(ctx.author.id)
    saldo = banco.get(usuario_id, 0)
    embed = discord.Embed(
        title="🏦 Banco de Runas",
        description=f"Consulta de saldo para **{ctx.author.name}**",
        color=0x0099FF,
    )

    embed.add_field(name="Saldo Actual", value=f"💰 {saldo} monedas", inline=False)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text="Rez Bot - El mago de las runas")

    await ctx.send(embed=embed)


@bot.command()
@commands.cooldown(1, 180, commands.BucketType.user)
async def trabajar(ctx):
    numero = random.randint(50, 2000)
    usuario_id = str(ctx.author.id)
    usuario_balance = banco.get(usuario_id, 0)
    banco[usuario_id] = usuario_balance + numero

    if numero >= 1000:
        embed = discord.Embed(
            title="¡Gran Trabajo!",
            description=f"¡Increíble {ctx.author.name}! Hoy has ganado {numero} monedas.",
            color=0x2ECC71,
        )
    else:
        embed = discord.Embed(
            title="Buen Trabajo",
            description=f"¡Bien hecho {ctx.author.name}! Hoy has ganado {numero} monedas.",
            color=0xE74C3C,
        )

    guardar_banco()
    await ctx.send(embed=embed)


@bot.command()
async def robar(ctx, victima: discord.Member):
    ladron_id = str(ctx.author.id)
    victima_id = str(victima.id)
    victima_balance = banco.get(victima_id, 0)

    suerte = random.randint(1, 100)
    if suerte > 50:
        ladron_balance = banco.get(ladron_id, 0)
        banco[ladron_id] = ladron_balance - 100
        guardar_banco()
        await ctx.send(
            f"Hola {ctx.author.name}, has fallado el intento de robo a {victima.name} "
            "y se te ha castigado con una multa de 100 monedas."
        )
        return

    if victima_balance <= 0:
        await ctx.send(f"{victima.name} no tiene monedas para robar.")
        return

    cantidad_a_robar = random.randint(1, victima_balance)
    banco[victima_id] = victima_balance - cantidad_a_robar
    ladron_balance = banco.get(ladron_id, 0)
    banco[ladron_id] = ladron_balance + cantidad_a_robar
    guardar_banco()

    await ctx.send(
        f"Hola {ctx.author.name}, has robado exitosamente "
        f"{cantidad_a_robar} monedas a {victima.name}."
    )


@bot.command()
async def donar(ctx, receptor: discord.Member, cantidad: str):
    try:
        cantidad = int(cantidad)
    except ValueError:
        await ctx.send("¡Oye! Tienes que poner un número de monedas válido.")
        return

    donante_id = str(ctx.author.id)
    receptor_id = str(receptor.id)
    donante_balance = banco.get(donante_id, 0)

    if cantidad < 200:
        await ctx.send("No puedes donar menos de 200 monedas.")
        return

    if cantidad > donante_balance:
        await ctx.send("¡Oye! No tienes suficientes monedas para donar esa cantidad.")
        return

    banco[donante_id] = donante_balance - cantidad
    receptor_balance = banco.get(receptor_id, 0)
    banco[receptor_id] = receptor_balance + cantidad
    guardar_banco()

    await ctx.send(
        f"Gracias por completar la transferencia de {cantidad} monedas "
        f"a {receptor.name}."
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"¡Cálmate! Inténtalo de nuevo en {round(error.retry_after, 2)} segundos."
        )


@bot.command()
async def ranking(ctx):
    ranking_usuario = sorted(banco.items(), key=lambda x: x[1], reverse=True)
    embed = discord.Embed(
        title="🏦 Los 5 más ricos del servidor",
        description="🏆 **Top 5 usuarios más ricos en el servidor** 🏆",
        color=0x0099FF,
    )

    for i, (id_usuario, saldo) in enumerate(ranking_usuario[:5], start=1):
        try:
            usuario = await bot.fetch_user(int(id_usuario))
            nombre_usuario = usuario.name
        except discord.DiscordException:
            nombre_usuario = "Viajero desconocido"

        embed.add_field(
            name=f"{i}. {nombre_usuario}",
            value=f"💰 {saldo} monedas",
            inline=False,
        )

    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f"{bot.user} ha iniciado sesión en Discord!")


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN no está configurado.")

bot.run(TOKEN)
