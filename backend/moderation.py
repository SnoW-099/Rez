import discord
from discord.ext import commands
from datetime import timedelta
from bank_system import BankSystem
from commands_manager import increment_command_count
import logging

logger = logging.getLogger(__name__)

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason specified"):
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't warn someone with equal or higher role.")
            return
        
        warnings = self.bank.add_warning(member.id)
        
        embed = discord.Embed(title="⚠️ User Warned", color=0xffa500)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Warnings", value=f"{warnings}/3", inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        
        await ctx.send(embed=embed)
        
        if warnings >= 3:
            try:
                await member.kick(reason="3 warnings accumulated")
                await ctx.send(f"👢 **{member.display_name}** was kicked for 3 warnings.")
                self.bank.reset_warnings(member.id)
            except discord.Forbidden:
                await ctx.send("❌ I don't have permission to kick.")

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need manage messages permission.")

    @commands.command(name='mute', aliases=['timeout'])
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: str = "10m", *, reason: str = "No reason"):
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't mute someone with equal or higher role.")
            return
        
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        unit = duration[-1].lower()
        
        if unit not in time_units:
            await ctx.send("❌ Invalid format. Use: `10s`, `5m`, `1h`, `1d`")
            return
        
        try:
            amount = int(duration[:-1])
        except ValueError:
            await ctx.send("❌ Invalid amount.")
            return
        
        seconds = amount * time_units[unit]
        if seconds > 2419200:
            await ctx.send("❌ Maximum is 28 days.")
            return
        
        try:
            await member.timeout(timedelta(seconds=seconds), reason=reason)
            
            embed = discord.Embed(title="🔇 User Muted", color=0xff6b6b)
            embed.add_field(name="User", value=member.mention, inline=True)
            embed.add_field(name="Duration", value=duration, inline=True)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            logger.info(f"Mute: {member} for {duration} - {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to mute this user.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need moderate members permission.")

    @commands.command(name='unmute', aliases=['untimeout'])
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        increment_command_count()
        
        try:
            await member.timeout(None)
            await ctx.send(f"🔊 **{member.display_name}** can speak again.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unmute.")

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't ban someone with equal or higher role.")
            return
        
        try:
            try:
                await member.send(f"🚫 You have been banned from **{ctx.guild.name}**\nReason: {reason}")
            except:
                pass
            
            await member.ban(reason=reason, delete_message_days=1)
            
            embed = discord.Embed(title="🔨 User Banned", color=0xff0000)
            embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            logger.info(f"Ban: {member} - {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to ban this user.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need ban members permission.")

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        increment_command_count()
        
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"✅ **{user}** has been unbanned.")
        except discord.NotFound:
            await ctx.send("❌ User not found or not banned.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unban.")

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        increment_command_count()
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't kick someone with equal or higher role.")
            return
        
        try:
            try:
                await member.send(f"👢 You have been kicked from **{ctx.guild.name}**\nReason: {reason}")
            except:
                pass
            
            await member.kick(reason=reason)
            
            embed = discord.Embed(title="👢 User Kicked", color=0xffa500)
            embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            
            await ctx.send(embed=embed)
            logger.info(f"Kick: {member} - {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to kick this user.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need kick members permission.")

    @commands.command(name='clear', aliases=['purge', 'clean'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        increment_command_count()
        
        if amount < 1 or amount > 100:
            await ctx.send("❌ Amount must be between 1 and 100.")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"🗑️ Deleted **{len(deleted) - 1}** messages.", delete_after=5)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to delete messages.")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need manage messages permission.")

    @commands.command(name='slowmode', aliases=['slow'])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        increment_command_count()
        
        if seconds < 0 or seconds > 21600:
            await ctx.send("❌ Slowmode must be between 0 and 21600 seconds (6 hours).")
            return
        
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                await ctx.send("⚡ Slowmode disabled.")
            else:
                await ctx.send(f"🐌 Slowmode set to **{seconds}** seconds.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to change slowmode.")

    @commands.command(name='reset_warnings', aliases=['clearwarns'])
    @commands.has_permissions(manage_messages=True)
    async def reset_warnings(self, ctx, member: discord.Member):
        increment_command_count()
        
        self.bank.reset_warnings(member.id)
        await ctx.send(f"✅ Warnings for **{member.display_name}** have been reset.")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))