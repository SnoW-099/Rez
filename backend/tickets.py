import discord
from discord.ext import commands
from datetime import datetime
from commands_manager import increment_command_count
import logging

logger = logging.getLogger(__name__)

class TicketsCog(commands.Cog):
    """Sistema de tickets de soporte"""
    
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 0
        self.active_tickets = {}

    @commands.command(name='ticket', aliases=['soporte', 'support'])
    async def create_ticket(self, ctx, *, reason: str = "Sin razón especificada"):
        """Crea un ticket de soporte"""
        increment_command_count()
        
        # Verificar si ya tiene un ticket abierto
        for ticket_id, ticket in self.active_tickets.items():
            if ticket['user_id'] == ctx.author.id:
                channel = self.bot.get_channel(ticket['channel_id'])
                if channel:
                    await ctx.send(f"❌ Ya tienes un ticket abierto: {channel.mention}")
                    return
        
        # Crear canal de ticket
        self.ticket_counter += 1
        ticket_name = f"ticket-{self.ticket_counter:04d}"
        
        # Buscar categoría de tickets o crear el canal directamente
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                attach_files=True
            ),
            ctx.guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                manage_channels=True
            )
        }
        
        # Añadir permisos para roles de staff
        for role in ctx.guild.roles:
            if role.permissions.manage_messages or role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True
                )
        
        try:
            channel = await ctx.guild.create_text_channel(
                ticket_name,
                overwrites=overwrites,
                reason=f"Ticket creado por {ctx.author}"
            )
            
            self.active_tickets[self.ticket_counter] = {
                'user_id': ctx.author.id,
                'channel_id': channel.id,
                'created_at': datetime.utcnow(),
                'reason': reason
            }
            
            embed = discord.Embed(
                title="🎫 Ticket de Soporte",
                description=f"Gracias por contactarnos, {ctx.author.mention}!\n\nUn miembro del staff te atenderá pronto.",
                color=0x5865F2
            )
            embed.add_field(name="Razón", value=reason, inline=False)
            embed.add_field(name="Cerrar", value="Usa `!close` para cerrar este ticket", inline=False)
            embed.set_footer(text=f"Ticket #{self.ticket_counter:04d}")
            
            await channel.send(ctx.author.mention, embed=embed)
            await ctx.send(f"✅ Ticket creado: {channel.mention}")
            
            logger.info(f"Ticket creado por {ctx.author}: {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ No tengo permisos para crear canales.")

    @commands.command(name='close', aliases=['cerrar', 'closeticket'])
    async def close_ticket(self, ctx):
        """Cierra el ticket actual"""
        increment_command_count()
        
        # Verificar si estamos en un canal de ticket
        ticket_id = None
        for tid, ticket in self.active_tickets.items():
            if ticket['channel_id'] == ctx.channel.id:
                ticket_id = tid
                break
        
        if ticket_id is None:
            await ctx.send("❌ Este no es un canal de ticket.")
            return
        
        ticket = self.active_tickets[ticket_id]
        
        # Verificar permisos (solo el creador o staff)
        if ctx.author.id != ticket['user_id'] and not ctx.author.guild_permissions.manage_messages:
            await ctx.send("❌ Solo el creador del ticket o el staff puede cerrarlo.")
            return
        
        embed = discord.Embed(
            title="🎫 Ticket Cerrado",
            description=f"Ticket cerrado por {ctx.author.mention}",
            color=0xef4444
        )
        embed.add_field(name="Creado por", value=f"<@{ticket['user_id']}>", inline=True)
        embed.add_field(name="Razón original", value=ticket['reason'], inline=False)
        
        await ctx.send(embed=embed)
        await ctx.send("Este canal se eliminará en 5 segundos...")
        
        # Esperar y eliminar
        import asyncio
        await asyncio.sleep(5)
        
        try:
            del self.active_tickets[ticket_id]
            await ctx.channel.delete(reason="Ticket cerrado")
            logger.info(f"Ticket #{ticket_id} cerrado por {ctx.author}")
        except discord.Forbidden:
            await ctx.send("❌ No puedo eliminar el canal.")

    @commands.command(name='adduser', aliases=['ticketadd'])
    @commands.has_permissions(manage_messages=True)
    async def add_user_to_ticket(self, ctx, member: discord.Member):
        """Añade un usuario al ticket"""
        increment_command_count()
        
        # Verificar si estamos en un ticket
        is_ticket = any(t['channel_id'] == ctx.channel.id for t in self.active_tickets.values())
        
        if not is_ticket:
            await ctx.send("❌ Este no es un canal de ticket.")
            return
        
        await ctx.channel.set_permissions(
            member,
            read_messages=True,
            send_messages=True
        )
        
        await ctx.send(f"✅ {member.mention} ha sido añadido al ticket.")

    @commands.command(name='removeuser', aliases=['ticketremove'])
    @commands.has_permissions(manage_messages=True)
    async def remove_user_from_ticket(self, ctx, member: discord.Member):
        """Remueve un usuario del ticket"""
        increment_command_count()
        
        is_ticket = any(t['channel_id'] == ctx.channel.id for t in self.active_tickets.values())
        
        if not is_ticket:
            await ctx.send("❌ Este no es un canal de ticket.")
            return
        
        await ctx.channel.set_permissions(member, overwrite=None)
        await ctx.send(f"✅ {member.mention} ha sido removido del ticket.")

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))
