import random
from discord.ext import commands
import discord
from bank_system import banco, guardar_banco
from config import bot


@bot.command()
async def balance(ctx):
    usuario = str(ctx.author.id)
    usuario_balance = banco.get(usuario, 0)
    await ctx.send(f"hola {ctx.author.name}, tu saldo en el banco es de {usuario_balance} en el servidor")


@bot.command()
@commands.cooldown(1, 180, commands.BucketType.user)
async def trabajar(ctx):
    numero = random.randint(50, 2000)
    usuario = str(ctx.author.id)
    usuario_balance = banco.get(usuario, 0)
    banco[usuario] = usuario_balance + numero
    await ctx.send(f"hola {ctx.author.name}, tu trabajo te ha dado {numero} en el servidor")

    if numero > 1000:
        await ctx.send("¡Felicidades! hoy te levantaste con suerte!!")
    else:
        await ctx.send("bueno, dentro de lo que cabe no esta tan mal jajaja!!")
    guardar_banco()


@bot.command()
async def robar(ctx, victima: discord.Member):
    ladron_id = str(ctx.author.id)
    victima_id = str(victima.id)
    victima_balance = banco.get(victima_id, 0)

    suerte = random.randint(1, 100)
    if suerte > 50:
        await ctx.send(f"hola {ctx.author.name}, has fallado en el intento de robo a {victima.name} en el servidor y se te ha castigado conuna multa de 100")
        ladron_balance = banco.get(ladron_id, 0)
        banco[ladron_id] = ladron_balance - 100
        guardar_banco()
        return

    if victima_balance > 0:
        cantidad_a_robar = random.randint(1, victima_balance)
        banco[victima_id] = victima_balance - cantidad_a_robar
        ladron_balance = banco.get(ladron_id, 0)
        banco[ladron_id] = ladron_balance + cantidad_a_robar
        guardar_banco()

        await ctx.send(f"hola {ctx.author.name}, has robado exitosamente {cantidad_a_robar} a {victima.name} en el servidor")


@bot.command()
async def donar(ctx, receptor: discord.Member, cantidad: str):  # Recibimos la cantidad como texto
    try:
        cantidad = int(cantidad)  # Intentamos convertir
        donante_id = str(ctx.author.id)
        receptor_id = str(receptor.id)
        donante_balance = banco.get(donante_id, 0)
        if cantidad <= 200:
            await ctx.send("oye no pues no puedes donar cantidades negativas o cero el minimo son 200")
            return
        if cantidad > donante_balance:
            await ctx.send("¡Oye! No tienes suficientes monedas para donar esa cantidad.")
            return
        if cantidad >= 200:
            banco[donante_id] = donante_balance - cantidad
            receptor_balance = banco.get(receptor_id, 0)
            banco[receptor_id] = receptor_balance + cantidad
            await ctx.send(f"Gracias por completar la transferenecia de {cantidad} moenad a {receptor.name} en el servidor😊")
    except ValueError:
        await ctx.send("¡Oye! Tienes que poner un número de monedas válido.")

    guardar_banco()



@bot.command()
async def ranking(ctx):
    # 1. Ordenamos el diccionario 'banco'
    # .items() convierte el dict en una lista de tuplas [('id', saldo), ('id', saldo)]
    # sorted lo ordena de mayor a menor saldo usando reverse=True
    ranking_usuarios = sorted(banco.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(
        title="🏆 Los 5 más ricos del Server",
        description="Aquí están los usuarios con más runas acumuladas hasta ahora.",
        color=0xFFA500 # Naranja Rez
    )

    # 2. Recorremos los primeros 5 puestos
    for i, (id_usuario, saldo) in enumerate(ranking_usuarios[:5], start=1):
        try:
            # Buscamos el objeto usuario para obtener su nombre real
            usuario = await bot.fetch_user(int(id_usuario))
            nombre_usuario = usuario.name
        except:
            # Por si el usuario ya no está en el servidor o hay un error
            nombre_usuario = "Viajero desconocido"

        embed.add_field(
            name=f"{i}. {nombre_usuario}",
            value=f"💰 {saldo} monedas",
            inline=False  
        )

    embed.set_footer(text="Rez Bot - El mago de las runas")
    
    await ctx.send(embed=embed)