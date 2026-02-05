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
        """Shows a user's profile"""
        increment_command_count()
        if member is None:
            member = ctx.author
        
        user_data = self.bank.get_user_data(member.id)
        
        embed = discord.Embed(
            title=f"👤 {member.display_name}'s Profile",
            color=0x5865F2
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Economy
        embed.add_field(name="💰 Balance", value=f"${user_data['balance']:,}", inline=True)
        embed.add_field(name="📊 Total Earned", value=f"${user_data.get('total_earned', 0):,}", inline=True)
        embed.add_field(name="💸 Total Spent", value=f"${user_data.get('total_spent', 0):,}", inline=True)
        
        # XP and Level
        level = user_data.get('level', 0)
        xp = user_data.get('xp', 0)
        next_level_xp = self.bank.xp_for_level(level + 1)
        
        embed.add_field(name="⭐ Level", value=str(level), inline=True)
        embed.add_field(name="✨ XP", value=f"{xp:,} / {next_level_xp:,}", inline=True)
        embed.add_field(name="💬 Messages", value=f"{user_data.get('messages', 0):,}", inline=True)
        
        # Moderation
        embed.add_field(name="⚠️ Warnings", value=str(user_data['warnings']), inline=True)
        
        embed.set_footer(text=f"ID: {member.id}")
        await ctx.send(embed=embed)

    @commands.command(name='ranking')
    async def ranking(self, ctx):
        """Shows top 5 richest users"""
        increment_command_count()
        top_users = self.bank.get_top_users(5)
        
        embed = discord.Embed(title="🏆 Top 5 Richest Users", color=0xffd700)
        
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        for i, (user_id, data) in enumerate(top_users):
            try:
                user = await self.bot.fetch_user(int(user_id))
                username = user.name
            except:
                username = f"User {user_id[:8]}..."
            
            embed.add_field(
                name=f"{medals[i]} {username}",
                value=f"${data['balance']:,}",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='work')
    async def work(self, ctx):
        """Work to earn money (cooldown: 3 minutes)"""
        increment_command_count()
        user_id = ctx.author.id
        
        remaining = self.bank.get_cooldown(user_id, 'work')
        if remaining > 0:
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            await ctx.send(f"⏰ Wait **{minutes}m {seconds}s** to work again.")
            return
        
        earnings = random.randint(50, 200)
        self.bank.add_money(user_id, earnings)
        self.bank.set_cooldown(user_id, 'work', 180)
        
        messages = [
            f"💼 You worked at the office and earned **${earnings}**!",
            f"🏗️ You helped at construction and got paid **${earnings}**!",
            f"🍕 You delivered pizzas and earned **${earnings}** in tips!",
            f"💻 You coded for a few hours and earned **${earnings}**!",
            f"🎨 You sold a drawing for **${earnings}**!"
        ]
        
        await ctx.send(random.choice(messages))

    @commands.command(name='daily')
    async def daily(self, ctx):
        """Collect your daily reward"""
        increment_command_count()
        user_id = ctx.author.id
        
        remaining = self.bank.get_cooldown(user_id, 'daily')
        if remaining > 0:
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            await ctx.send(f"⏰ Already collected. Come back in **{hours}h {minutes}m**.")
            return
        
        reward = random.randint(200, 500)
        self.bank.add_money(user_id, reward)
        self.bank.set_cooldown(user_id, 'daily', 86400)
        
        await ctx.send(f"🎁 You collected your daily reward of **${reward}**!")

    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your balance or another user's"""
        increment_command_count()
        if member is None:
            member = ctx.author
        
        user_data = self.bank.get_user_data(member.id)
        await ctx.send(f"💰 **{member.display_name}** has **${user_data['balance']:,}**")

    @commands.command(name='transfer', aliases=['pay', 'give'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfer money to another user"""
        increment_command_count()
        
        if member.id == ctx.author.id:
            await ctx.send("❌ You can't transfer money to yourself.")
            return
        
        if amount <= 0:
            await ctx.send("❌ Amount must be greater than 0.")
            return
        
        sender_data = self.bank.get_user_data(ctx.author.id)
        if sender_data['balance'] < amount:
            await ctx.send("❌ You don't have enough money.")
            return
        
        self.bank.remove_money(ctx.author.id, amount)
        self.bank.add_money(member.id, amount)
        
        embed = discord.Embed(
            title="💸 Transfer Complete",
            color=0x10b981
        )
        embed.add_field(name="From", value=ctx.author.mention, inline=True)
        embed.add_field(name="To", value=member.mention, inline=True)
        embed.add_field(name="Amount", value=f"${amount:,}", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='rob', aliases=['steal'])
    async def rob(self, ctx, member: discord.Member):
        """Try to rob another user (50% success)"""
        increment_command_count()
        
        if member.id == ctx.author.id:
            await ctx.send("❌ You can't rob yourself.")
            return
        
        if member.bot:
            await ctx.send("❌ You can't rob bots.")
            return
        
        remaining = self.bank.get_cooldown(ctx.author.id, 'rob')
        if remaining > 0:
            minutes = int(remaining // 60)
            await ctx.send(f"⏰ Wait **{minutes}m** to rob again.")
            return
        
        victim_data = self.bank.get_user_data(member.id)
        if victim_data['balance'] < 100:
            await ctx.send(f"❌ **{member.display_name}** doesn't have enough money to rob.")
            return
        
        self.bank.set_cooldown(ctx.author.id, 'rob', 300)
        
        if random.random() < 0.5:
            stolen = random.randint(50, min(500, victim_data['balance']))
            self.bank.remove_money(member.id, stolen)
            self.bank.add_money(ctx.author.id, stolen)
            await ctx.send(f"💰 You robbed **${stolen}** from {member.mention}!")
        else:
            fine = random.randint(50, 150)
            self.bank.remove_money(ctx.author.id, fine)
            await ctx.send(f"🚔 You were caught! You paid **${fine}** in fines.")

    @commands.command(name='shop', aliases=['store', 'tienda'])
    async def shop(self, ctx):
        """View the item shop"""
        increment_command_count()
        
        embed = discord.Embed(
            title="🛒 Item Shop",
            description="Buy items with `!buy [item]`",
            color=0x5865F2
        )
        
        items = [
            ("🎣 Fishing Rod", "fishing_rod", 500, "Fish for money"),
            ("⛏️ Pickaxe", "pickaxe", 750, "Mine for minerals"),
            ("🎰 Lucky Coin", "lucky_coin", 1000, "+10% casino wins"),
            ("💼 Briefcase", "briefcase", 2000, "+25% work earnings"),
            ("🛡️ Shield", "shield", 1500, "Protection from robbers")
        ]
        
        for emoji_name, item_id, price, desc in items:
            embed.add_field(
                name=f"{emoji_name} - ${price:,}",
                value=f"`!buy {item_id}`\n{desc}",
                inline=True
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='buy', aliases=['purchase'])
    async def buy(self, ctx, item: str = None):
        """Buy an item from the shop"""
        increment_command_count()
        
        if item is None:
            await ctx.send("❌ Specify an item. Use `!shop` to see available items.")
            return
        
        items = {
            "fishing_rod": ("🎣 Fishing Rod", 500),
            "pickaxe": ("⛏️ Pickaxe", 750),
            "lucky_coin": ("🎰 Lucky Coin", 1000),
            "briefcase": ("💼 Briefcase", 2000),
            "shield": ("🛡️ Shield", 1500)
        }
        
        item = item.lower()
        if item not in items:
            await ctx.send("❌ Item not found. Use `!shop`.")
            return
        
        name, price = items[item]
        user_data = self.bank.get_user_data(ctx.author.id)
        
        if user_data['balance'] < price:
            await ctx.send(f"❌ You need **${price:,}** to buy this.")
            return
        
        self.bank.remove_money(ctx.author.id, price)
        
        embed = discord.Embed(
            title="✅ Purchase Complete!",
            description=f"You bought **{name}** for **${price:,}**",
            color=0x10b981
        )
        await ctx.send(embed=embed)

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot latency"""
        increment_command_count()
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: **{latency}ms**")

    @commands.command(name='help', aliases=['commands', 'h'])
    async def help_command(self, ctx):
        """Show all available commands"""
        increment_command_count()
        
        embed = discord.Embed(
            title="📚 Rez Bot Commands",
            description="Use `!command` to run a command",
            color=0x5865F2
        )
        
        embed.add_field(
            name="💰 Economy",
            value="`profile` `balance` `work` `daily` `transfer` `rob` `ranking` `shop` `buy`",
            inline=False
        )
        
        embed.add_field(
            name="⭐ Levels",
            value="`level` `leaderboard`",
            inline=False
        )
        
        embed.add_field(
            name="🎰 Casino",
            value="`coinflip` `slots` `blackjack` `roulette`",
            inline=False
        )
        
        embed.add_field(
            name="🎁 Giveaways",
            value="`giveaway` `gend` `greroll`",
            inline=False
        )
        
        embed.add_field(
            name="🎫 Tickets",
            value="`ticket` `close`",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Moderation",
            value="`warn` `mute` `unmute` `kick` `ban` `unban` `clear` `slowmode`",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Utility",
            value="`ping` `help`",
            inline=False
        )
        
        embed.set_footer(text="Rez Bot v2.0 - Liquid Black Edition")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandsCog(bot))