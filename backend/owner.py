import discord
from discord.ext import commands
from bank_system import BankSystem
from commands_manager import increment_command_count
import logging

logger = logging.getLogger(__name__)

OWNER_ID = 972405071902023711

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    @commands.command(name='addmoney', aliases=['addbal', 'givemoney'])
    @is_owner()
    async def add_money(self, ctx, member: discord.Member, amount: int):
        increment_command_count()
        if amount <= 0:
            await ctx.send("Amount must be positive.")
            return
        self.bank.add_money(member.id, amount)
        embed = discord.Embed(title="Money Added", color=0xffffff)
        embed.add_field(name="User",   value=member.mention,  inline=True)
        embed.add_field(name="Amount", value=f"+${amount:,}", inline=True)
        embed.add_field(name="By",     value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} added ${amount} to {member}")

    @commands.command(name='removemoney', aliases=['removebal', 'takemoney'])
    @is_owner()
    async def remove_money(self, ctx, member: discord.Member, amount: int):
        increment_command_count()
        if amount <= 0:
            await ctx.send("Amount must be positive.")
            return
        actual = self.bank.remove_money(member.id, amount)
        embed = discord.Embed(title="Money Removed", color=0xffffff)
        embed.add_field(name="User",   value=member.mention, inline=True)
        embed.add_field(name="Amount", value=f"-${actual:,}", inline=True)
        embed.add_field(name="By",     value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} removed ${actual} from {member}")

    @commands.command(name='setlevel')
    @is_owner()
    async def set_level(self, ctx, member: discord.Member, level: int):
        increment_command_count()
        if level < 0:
            await ctx.send("Level cannot be negative.")
            return
        xp_needed = self.bank.xp_for_level(level)
        # Use bank's db shim so it works in both MongoDB and JSON mode
        data = self.bank.get_user_data(member.id)
        if hasattr(self.bank, '_set_fields'):
            self.bank._set_fields(member.id, {'level': level, 'xp': xp_needed})
        else:
            from bank_system import _USE_MONGO, _mongo_db, _json_cache, _save
            if _USE_MONGO:
                _mongo_db.users.update_one({'user_id': str(member.id)}, {'$set': {'level': level, 'xp': xp_needed}})
            else:
                _json_cache[str(member.id)]['level'] = level
                _json_cache[str(member.id)]['xp'] = xp_needed
                _save()
        embed = discord.Embed(title="Level Set", color=0xffffff)
        embed.add_field(name="User",      value=member.mention, inline=True)
        embed.add_field(name="New Level", value=str(level),     inline=True)
        embed.add_field(name="XP",        value=f"{xp_needed:,}", inline=True)
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} set level {level} for {member}")

    @commands.command(name='resetuser')
    @is_owner()
    async def reset_user(self, ctx, member: discord.Member):
        increment_command_count()
        from bank_system import _USE_MONGO, _mongo_db, _json_cache, _save
        if _USE_MONGO:
            _mongo_db.users.delete_one({'user_id': str(member.id)})
        else:
            _json_cache.pop(str(member.id), None)
            _save()
        embed = discord.Embed(title="User Reset", description=f"All data for {member.mention} has been deleted.", color=0xffffff)
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} reset {member}")

    @commands.command(name='setbalance', aliases=['setbal'])
    @is_owner()
    async def set_balance(self, ctx, member: discord.Member, amount: int):
        increment_command_count()
        from bank_system import _USE_MONGO, _mongo_db, _json_cache, _save
        if _USE_MONGO:
            _mongo_db.users.update_one({'user_id': str(member.id)}, {'$set': {'balance': amount}}, upsert=True)
        else:
            data = self.bank.get_user_data(member.id)
            _json_cache[str(member.id)]['balance'] = amount
            _save()
        embed = discord.Embed(title="Balance Set", color=0xffffff)
        embed.add_field(name="User",        value=member.mention, inline=True)
        embed.add_field(name="New Balance", value=f"${amount:,}", inline=True)
        await ctx.send(embed=embed)
        logger.info(f"[OWNER] {ctx.author} set balance ${amount} for {member}")

    @commands.command(name='botstat')
    @is_owner()
    async def botstats(self, ctx):
        increment_command_count()
        embed = discord.Embed(title="Bot Statistics", color=0xffffff)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users",   value=len(self.bot.users), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        stats = self.bank.get_stats()
        embed.add_field(name="DB Users",    value=stats.get('total_users', 0),    inline=True)
        embed.add_field(name="Total Coins", value=f"${stats.get('total_coins', 0):,}", inline=True)
        await ctx.send(embed=embed)

    @add_money.error
    @remove_money.error
    @set_level.error
    @reset_user.error
    @set_balance.error
    @botstats.error
    async def owner_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the bot owner can use this command.")
        else:
            logger.error(f"Error in owner command: {error}")

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
