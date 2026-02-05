import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta
from commands_manager import increment_command_count
import logging

logger = logging.getLogger(__name__)

class GiveawayCog(commands.Cog):
    """Giveaway system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}

    @commands.command(name='giveaway', aliases=['gstart'])
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx, duration: str, *, prize: str):
        """Create a giveaway. Usage: !giveaway 1h Special Prize"""
        increment_command_count()
        
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        unit = duration[-1].lower()
        
        if unit not in time_units:
            await ctx.send("❌ Invalid format. Use: `1m`, `1h`, `1d`")
            return
        
        try:
            amount = int(duration[:-1])
        except ValueError:
            await ctx.send("❌ Invalid duration.")
            return
        
        seconds = amount * time_units[unit]
        if seconds > 604800:
            await ctx.send("❌ Maximum 7 days.")
            return
        
        end_time = datetime.utcnow() + timedelta(seconds=seconds)
        
        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description=f"**Prize:** {prize}\n\nReact with 🎁 to enter!",
            color=0x10b981
        )
        embed.add_field(name="Ends in", value=f"<t:{int(end_time.timestamp())}:R>", inline=True)
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
        
        await asyncio.sleep(seconds)
        await self.end_giveaway(msg.id)

    async def end_giveaway(self, message_id):
        """End a giveaway and pick winner"""
        if message_id not in self.active_giveaways:
            return
        
        giveaway = self.active_giveaways.pop(message_id)
        
        try:
            channel = self.bot.get_channel(giveaway['channel_id'])
            message = await channel.fetch_message(message_id)
            
            users = []
            for reaction in message.reactions:
                if str(reaction.emoji) == "🎁":
                    async for user in reaction.users():
                        if not user.bot:
                            users.append(user)
            
            if not users:
                embed = discord.Embed(
                    title="🎉 Giveaway Ended",
                    description="No participants 😢",
                    color=0xef4444
                )
                await channel.send(embed=embed)
                return
            
            winner = random.choice(users)
            
            embed = discord.Embed(
                title="🎉 We Have a Winner!",
                description=f"**Prize:** {giveaway['prize']}\n\n🏆 **Winner:** {winner.mention}",
                color=0x10b981
            )
            embed.set_thumbnail(url=winner.avatar.url if winner.avatar else winner.default_avatar.url)
            
            await channel.send(f"🎊 Congratulations {winner.mention}!", embed=embed)
            logger.info(f"Giveaway ended: {winner} won '{giveaway['prize']}'")
            
        except Exception as e:
            logger.error(f"Error ending giveaway: {e}")

    @commands.command(name='gend', aliases=['endgiveaway'])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_end(self, ctx, message_id: int = None):
        """End a giveaway manually"""
        increment_command_count()
        
        if message_id is None:
            if not self.active_giveaways:
                await ctx.send("❌ No active giveaways.")
                return
            message_id = list(self.active_giveaways.keys())[-1]
        
        if message_id not in self.active_giveaways:
            await ctx.send("❌ Giveaway not found.")
            return
        
        await self.end_giveaway(message_id)
        await ctx.send("✅ Giveaway ended!")

    @commands.command(name='greroll', aliases=['reroll'])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_reroll(self, ctx, message_id: int):
        """Reroll a giveaway winner"""
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
                await ctx.send("❌ No participants.")
                return
            
            winner = random.choice(users)
            await ctx.send(f"🎊 New winner: {winner.mention}!")
            
        except discord.NotFound:
            await ctx.send("❌ Message not found.")

async def setup(bot):
    await bot.add_cog(GiveawayCog(bot))
