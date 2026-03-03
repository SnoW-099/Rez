import discord
from discord.ext import commands
import random
from bank_system import BankSystem
from commands_manager import increment_command_count

class LevelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return

        try:
            xp_gained = random.randint(5, 15)
            leveled_up, new_level = self.bank.add_xp(message.author.id, xp_gained)

            if leveled_up:
                bonus = new_level * 100
                self.bank.add_money(message.author.id, bonus)

                embed = discord.Embed(
                    title="🎉 Level Up!",
                    description=f"{message.author.mention} reached **Level {new_level}**!",
                    color=0x10b981
                )
                embed.add_field(name="💰 Reward", value=f"+**${bonus:,}**", inline=True)
                embed.add_field(name="⭐ New Level", value=f"**{new_level}**", inline=True)
                embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)

                try:
                    await message.channel.send(embed=embed, delete_after=10)
                except Exception:
                    pass
        except Exception:
            pass  # Silently ignore DB errors on message events

    @commands.command(name='level', aliases=['lvl', 'xp'])
    async def level(self, ctx, member: discord.Member = None):
        increment_command_count()

        if member is None:
            member = ctx.author

        try:
            user_data = self.bank.get_user_data(member.id)
        except Exception:
            await ctx.send("❌ Could not connect to database.")
            return

        current_level = user_data.get('level', 0)
        current_xp = user_data.get('xp', 0)
        xp_for_next = self.bank.xp_for_level(current_level + 1)
        xp_for_current = self.bank.xp_for_level(current_level)

        xp_progress = current_xp - xp_for_current
        xp_needed = max(1, xp_for_next - xp_for_current)
        progress_percent = min(100, int((xp_progress / xp_needed) * 100))

        filled = progress_percent // 10
        bar = "█" * filled + "░" * (10 - filled)

        embed = discord.Embed(
            title=f"⭐ {member.display_name}'s Level",
            color=0x8b5cf6
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="⭐ Level", value=f"**{current_level}**", inline=True)
        embed.add_field(name="✨ Total XP", value=f"`{current_xp:,}`", inline=True)
        embed.add_field(name="📊 Progress", value=f"`{bar}` **{progress_percent}%**\n`{xp_progress:,} / {xp_needed:,} XP`", inline=False)
        embed.set_footer(text="Keep chatting to gain XP!")

        await ctx.send(embed=embed)

    @commands.command(name='leaderboard', aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        increment_command_count()

        try:
            users = list(self.bank.db.users.find().sort('xp', -1).limit(10))
        except Exception:
            await ctx.send("❌ Could not connect to database.")
            return

        if not users:
            await ctx.send("No users in the database yet! Start chatting to earn XP.")
            return

        embed = discord.Embed(title="🏆 XP Leaderboard", color=0x8b5cf6)
        medals = ['🥇', '🥈', '🥉']
        description = ""

        for i, user in enumerate(users):
            medal = medals[i] if i < 3 else f"`{i+1}.`"
            user_id = user.get('user_id')
            level = user.get('level', 0)
            xp = user.get('xp', 0)
            description += f"{medal} <@{user_id}> — Level **{level}** (`{xp:,} XP`)\n"

        embed.description = description
        embed.set_footer(text="Keep chatting to climb the ranks!")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(LevelsCog(bot))
