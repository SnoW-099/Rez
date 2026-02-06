import discord
from discord.ext import commands
from datetime import datetime
from commands_manager import increment_command_count
import logging
import asyncio

logger = logging.getLogger(__name__)

class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 0
        self.active_tickets = {}

    @commands.command(name='ticket', aliases=['support'])
    async def create_ticket(self, ctx, *, reason: str = "No reason specified"):
        increment_command_count()
        
        for ticket_id, ticket in self.active_tickets.items():
            if ticket['user_id'] == ctx.author.id:
                channel = self.bot.get_channel(ticket['channel_id'])
                if channel:
                    await ctx.send(f"❌ You already have an open ticket: {channel.mention}")
                    return
        
        self.ticket_counter += 1
        ticket_name = f"ticket-{self.ticket_counter:04d}"
        
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
                reason=f"Ticket created by {ctx.author}"
            )
            
            self.active_tickets[self.ticket_counter] = {
                'user_id': ctx.author.id,
                'channel_id': channel.id,
                'created_at': datetime.utcnow(),
                'reason': reason
            }
            
            embed = discord.Embed(
                title="🎫 Support Ticket",
                description=f"Thanks for contacting us, {ctx.author.mention}!\n\nA staff member will assist you soon.",
                color=0x5865F2
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Close", value="Use `!close` to close this ticket", inline=False)
            embed.set_footer(text=f"Ticket #{self.ticket_counter:04d}")
            
            await channel.send(ctx.author.mention, embed=embed)
            await ctx.send(f"✅ Ticket created: {channel.mention}")
            
            logger.info(f"Ticket created by {ctx.author}: {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to create channels.")

    @commands.command(name='close', aliases=['closeticket'])
    async def close_ticket(self, ctx):
        increment_command_count()
        
        ticket_id = None
        for tid, ticket in self.active_tickets.items():
            if ticket['channel_id'] == ctx.channel.id:
                ticket_id = tid
                break
        
        if ticket_id is None:
            await ctx.send("❌ This is not a ticket channel.")
            return
        
        ticket = self.active_tickets[ticket_id]
        
        if ctx.author.id != ticket['user_id'] and not ctx.author.guild_permissions.manage_messages:
            await ctx.send("❌ Only the ticket creator or staff can close it.")
            return
        
        embed = discord.Embed(
            title="🎫 Ticket Closed",
            description=f"Ticket closed by {ctx.author.mention}",
            color=0xef4444
        )
        embed.add_field(name="Created by", value=f"<@{ticket['user_id']}>", inline=True)
        embed.add_field(name="Original reason", value=ticket['reason'], inline=False)
        
        await ctx.send(embed=embed)
        await ctx.send("This channel will be deleted in 5 seconds...")
        
        await asyncio.sleep(5)
        
        try:
            del self.active_tickets[ticket_id]
            await ctx.channel.delete(reason="Ticket closed")
            logger.info(f"Ticket #{ticket_id} closed by {ctx.author}")
        except discord.Forbidden:
            await ctx.send("❌ I can't delete the channel.")

    @commands.command(name='adduser', aliases=['ticketadd'])
    @commands.has_permissions(manage_messages=True)
    async def add_user_to_ticket(self, ctx, member: discord.Member):
        increment_command_count()
        
        is_ticket = any(t['channel_id'] == ctx.channel.id for t in self.active_tickets.values())
        
        if not is_ticket:
            await ctx.send("❌ This is not a ticket channel.")
            return
        
        await ctx.channel.set_permissions(
            member,
            read_messages=True,
            send_messages=True
        )
        
        await ctx.send(f"✅ {member.mention} has been added to the ticket.")

    @commands.command(name='removeuser', aliases=['ticketremove'])
    @commands.has_permissions(manage_messages=True)
    async def remove_user_from_ticket(self, ctx, member: discord.Member):
        increment_command_count()
        
        is_ticket = any(t['channel_id'] == ctx.channel.id for t in self.active_tickets.values())
        
        if not is_ticket:
            await ctx.send("❌ This is not a ticket channel.")
            return
        
        await ctx.channel.set_permissions(member, overwrite=None)
        await ctx.send(f"✅ {member.mention} has been removed from the ticket.")

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))
