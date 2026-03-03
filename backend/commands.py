import discord
from discord.ext import commands
import random
import logging
from bank_system import BankSystem
from commands_manager import increment_command_count

logger = logging.getLogger(__name__)

WHITE = 0xffffff  # White sidebar on all embeds

# ─── Views ────────────────────────────────────────────────────

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    def build_embed(self, category: str) -> discord.Embed:
        pages = {
            "economy": ("Economy", [
                ("!balance", "Check your balance"),
                ("!work", "Earn coins (3 min cooldown)"),
                ("!daily", "Daily reward (24 h cooldown)"),
                ("!profile", "Your full profile"),
                ("!transfer @user amount", "Send coins to someone"),
                ("!rob @user", "Attempt to steal (50/50)"),
                ("!ranking", "Top 5 wealthiest"),
                ("!shop", "Item shop"),
            ]),
            "levels": ("Levels", [
                ("!level", "Your XP and level"),
                ("!leaderboard", "Top 10 by XP"),
            ]),
            "casino": ("Casino", [
                ("!coinflip amount heads/tails", "Coin flip bet"),
                ("!slots amount", "Slot machine"),
                ("!blackjack amount", "Blackjack"),
                ("!roulette amount red/black", "Roulette"),
            ]),
            "moderation": ("Moderation", [
                ("!warn @user reason", "Warn a user (3 = kick)"),
                ("!mute @user time", "Mute a user"),
                ("!kick @user", "Kick from server"),
                ("!ban @user", "Permanently ban"),
                ("!clear 1-100", "Bulk delete messages"),
                ("!slowmode seconds", "Set channel slowmode"),
            ]),
            "utility": ("Utility", [
                ("!ping", "Bot latency"),
                ("!ticket reason", "Open a support ticket"),
                ("!giveaway time prize", "Start a giveaway (admin)"),
                ("!close", "Close a ticket"),
            ]),
        }
        title, cmds = pages.get(category, pages["economy"])
        embed = discord.Embed(title=title, color=WHITE)
        for cmd, desc in cmds:
            embed.add_field(name=f"`{cmd}`", value=desc, inline=True)
        embed.set_footer(text="Rez Bot  ·  Select a category below")
        return embed

    @discord.ui.select(
        placeholder="Select a category…",
        options=[
            discord.SelectOption(label="Economy",    value="economy"),
            discord.SelectOption(label="Levels",     value="levels"),
            discord.SelectOption(label="Casino",     value="casino"),
            discord.SelectOption(label="Moderation", value="moderation"),
            discord.SelectOption(label="Utility",    value="utility"),
        ]
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.edit_message(embed=self.build_embed(select.values[0]), view=self)


class ShopView(discord.ui.View):
    ITEMS = {
        "fishing_rod": ("Fishing Rod",  500,  "Catch fish for bonus coins"),
        "pickaxe":     ("Pickaxe",      750,  "Mine for rare minerals"),
        "lucky_coin":  ("Lucky Coin",   1000, "+10% casino win rate"),
        "briefcase":   ("Briefcase",    2000, "+25% work earnings"),
        "shield":      ("Shield",       1500, "Blocks one rob attempt"),
    }

    def __init__(self, bank: BankSystem, buyer_id: int):
        super().__init__(timeout=60)
        self.bank = bank
        self.buyer_id = buyer_id

    @discord.ui.select(
        placeholder="Select an item to buy…",
        options=[
            discord.SelectOption(label="Fishing Rod ($500)",  value="fishing_rod",  description="Catch fish for bonus coins"),
            discord.SelectOption(label="Pickaxe ($750)",      value="pickaxe",      description="Mine for rare minerals"),
            discord.SelectOption(label="Lucky Coin ($1,000)", value="lucky_coin",   description="+10% casino win rate"),
            discord.SelectOption(label="Briefcase ($2,000)",  value="briefcase",    description="+25% work earnings"),
            discord.SelectOption(label="Shield ($1,500)",     value="shield",       description="Blocks one rob attempt"),
        ]
    )
    async def buy_item(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.buyer_id:
            await interaction.response.send_message("This isn't your shop.", ephemeral=True)
            return
        key = select.values[0]
        name, price, desc = self.ITEMS[key]
        data = self.bank.get_user_data(self.buyer_id)
        if data['balance'] < price:
            await interaction.response.send_message(
                f"Not enough funds. You need ${price:,} but have ${data['balance']:,}.", ephemeral=True
            )
            return
        self.bank.remove_money(self.buyer_id, price)
        embed = discord.Embed(title=f"{name} purchased", color=WHITE)
        embed.description = desc
        embed.add_field(name="Paid",        value=f"${price:,}",                   inline=True)
        embed.add_field(name="New balance", value=f"${data['balance'] - price:,}", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ─── Cog ─────────────────────────────────────────────────────

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()

    # ── Profile ────────────────────────────────────────────
    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        increment_command_count()
        if member is None:
            member = ctx.author
        async with ctx.typing():
            try:
                d = self.bank.get_user_data(member.id)
            except Exception as e:
                logger.error(e)
                await ctx.send("Could not reach the database.")
                return

        lvl     = d.get('level', 0)
        xp      = d.get('xp', 0)
        xp_next = self.bank.xp_for_level(lvl + 1)
        xp_cur  = self.bank.xp_for_level(lvl)
        xp_prog = max(0, xp - xp_cur)
        xp_need = max(1, xp_next - xp_cur)
        pct     = min(100, int(xp_prog / xp_need * 100))

        embed = discord.Embed(color=WHITE)
        embed.set_author(
            name=member.display_name,
            icon_url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Balance",      value=f"${d['balance']:,}",                  inline=True)
        embed.add_field(name="Total earned", value=f"${d.get('total_earned', 0):,}",      inline=True)
        embed.add_field(name="Messages",     value=f"{d.get('messages', 0):,}",           inline=True)
        embed.add_field(name="Level",        value=f"{lvl}",                              inline=True)
        embed.add_field(name="XP",           value=f"{xp_prog:,} / {xp_need:,}  ({pct}%)", inline=True)
        embed.add_field(name="Warnings",     value=str(d.get('warnings', 0)),             inline=True)
        embed.set_footer(text=f"ID: {member.id}  ·  Rez Bot")
        await ctx.send(embed=embed)

    # ── Ranking ────────────────────────────────────────────
    @commands.command(name='ranking')
    async def ranking(self, ctx):
        increment_command_count()
        async with ctx.typing():
            try:
                top = self.bank.get_top_users(5)
            except Exception:
                await ctx.send("Could not reach the database.")
                return

        medals = ["1.", "2.", "3.", "4.", "5."]
        desc = ""
        for i, (uid, data) in enumerate(top):
            try:
                user = await self.bot.fetch_user(int(uid))
                name = user.display_name
            except Exception:
                name = f"User #{str(uid)[:6]}"
            desc += f"`{medals[i]}`  **{name}** — ${data.get('balance', 0):,}\n"

        embed = discord.Embed(title="Richest Users", description=desc or "No users yet.", color=WHITE)
        embed.set_footer(text="Rez Bot  ·  !ranking")
        await ctx.send(embed=embed)

    # ── Work ───────────────────────────────────────────────
    @commands.command(name='work')
    async def work(self, ctx):
        increment_command_count()
        uid = ctx.author.id
        try:
            remaining = self.bank.get_cooldown(uid, 'work')
        except Exception:
            await ctx.send("Could not reach the database.")
            return

        if remaining > 0:
            m, s = int(remaining // 60), int(remaining % 60)
            embed = discord.Embed(description=f"You're on cooldown. Come back in **{m}m {s}s**.", color=WHITE)
            await ctx.send(embed=embed)
            return

        pay = random.randint(50, 200)
        self.bank.add_money(uid, pay)
        self.bank.set_cooldown(uid, 'work', 180)

        jobs = [
            "Finished a shift at the office",
            "Helped at a construction site",
            "Delivered orders across the city",
            "Shipped a client's feature",
            "Sold a digital commission",
            "Sorted packages at the warehouse",
        ]
        flavor = random.choice(jobs)
        embed = discord.Embed(color=WHITE)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.description = flavor
        embed.add_field(name="Earned",     value=f"${pay:,}",       inline=True)
        embed.add_field(name="Next shift", value="in 3 minutes",     inline=True)
        await ctx.send(embed=embed)

    # ── Daily ──────────────────────────────────────────────
    @commands.command(name='daily')
    async def daily(self, ctx):
        increment_command_count()
        uid = ctx.author.id
        try:
            remaining = self.bank.get_cooldown(uid, 'daily')
        except Exception:
            await ctx.send("Could not reach the database.")
            return

        if remaining > 0:
            h, m = int(remaining // 3600), int((remaining % 3600) // 60)
            embed = discord.Embed(description=f"Already claimed. Come back in **{h}h {m}m**.", color=WHITE)
            await ctx.send(embed=embed)
            return

        reward = random.randint(200, 500)
        self.bank.add_money(uid, reward)
        self.bank.set_cooldown(uid, 'daily', 86400)
        data = self.bank.get_user_data(uid)

        embed = discord.Embed(title="Daily reward", color=WHITE)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.add_field(name="Reward",      value=f"${reward:,}",        inline=True)
        embed.add_field(name="New balance", value=f"${data['balance']:,}", inline=True)
        embed.add_field(name="Next daily",  value="in 24 hours",          inline=True)
        await ctx.send(embed=embed)

    # ── Balance ────────────────────────────────────────────
    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        increment_command_count()
        if member is None:
            member = ctx.author
        try:
            d = self.bank.get_user_data(member.id)
        except Exception:
            await ctx.send("Could not reach the database.")
            return

        embed = discord.Embed(color=WHITE)
        embed.set_author(name=member.display_name, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Balance",      value=f"${d['balance']:,}",              inline=True)
        embed.add_field(name="Total earned", value=f"${d.get('total_earned', 0):,}",  inline=True)
        embed.add_field(name="Total spent",  value=f"${d.get('total_spent', 0):,}",   inline=True)
        await ctx.send(embed=embed)

    # ── Transfer ───────────────────────────────────────────
    @commands.command(name='transfer', aliases=['pay', 'give'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        increment_command_count()
        if member.id == ctx.author.id:
            await ctx.send("You can't pay yourself.")
            return
        if amount <= 0:
            await ctx.send("Amount must be positive.")
            return
        try:
            sender = self.bank.get_user_data(ctx.author.id)
        except Exception:
            await ctx.send("Could not reach the database.")
            return
        if sender['balance'] < amount:
            await ctx.send(f"Insufficient funds. You have ${sender['balance']:,}.")
            return
        self.bank.remove_money(ctx.author.id, amount)
        self.bank.add_money(member.id, amount)
        embed = discord.Embed(title="Transfer complete", color=WHITE)
        embed.add_field(name="From",   value=ctx.author.mention, inline=True)
        embed.add_field(name="To",     value=member.mention,     inline=True)
        embed.add_field(name="Amount", value=f"${amount:,}",     inline=True)
        await ctx.send(embed=embed)

    # ── Rob ────────────────────────────────────────────────
    @commands.command(name='rob', aliases=['steal'])
    async def rob(self, ctx, member: discord.Member):
        increment_command_count()
        if member.id == ctx.author.id or member.bot:
            await ctx.send("Invalid target.")
            return
        try:
            remaining = self.bank.get_cooldown(ctx.author.id, 'rob')
            victim    = self.bank.get_user_data(member.id)
        except Exception:
            await ctx.send("Could not reach the database.")
            return
        if remaining > 0:
            await ctx.send(f"Wait {int(remaining // 60)}m before robbing again.")
            return
        if victim['balance'] < 100:
            await ctx.send(f"{member.display_name} doesn't have enough to rob.")
            return
        self.bank.set_cooldown(ctx.author.id, 'rob', 300)
        if random.random() < 0.5:
            stolen = random.randint(50, min(500, victim['balance']))
            self.bank.remove_money(member.id, stolen)
            self.bank.add_money(ctx.author.id, stolen)
            embed = discord.Embed(description=f"Success. You took **${stolen:,}** from {member.mention}.", color=WHITE)
        else:
            fine = random.randint(50, 150)
            self.bank.remove_money(ctx.author.id, fine)
            embed = discord.Embed(description=f"Caught. You paid a **${fine:,}** fine.", color=WHITE)
        await ctx.send(embed=embed)

    # ── Shop ───────────────────────────────────────────────
    @commands.command(name='shop', aliases=['store'])
    async def shop(self, ctx):
        increment_command_count()
        embed = discord.Embed(title="Shop", color=WHITE)
        embed.description = "Select an item from the menu below to purchase it."
        embed.add_field(name="Fishing Rod",  value="$500  ·  Fish for bonus coins",   inline=False)
        embed.add_field(name="Pickaxe",      value="$750  ·  Mine for minerals",       inline=False)
        embed.add_field(name="Lucky Coin",   value="$1,000  ·  +10% casino win rate",  inline=False)
        embed.add_field(name="Briefcase",    value="$2,000  ·  +25% work earnings",    inline=False)
        embed.add_field(name="Shield",       value="$1,500  ·  Blocks a rob attempt",  inline=False)
        embed.set_footer(text="Rez Bot  ·  !balance to check your funds")
        await ctx.send(embed=embed, view=ShopView(self.bank, ctx.author.id))

    # ── Ping ───────────────────────────────────────────────
    @commands.command(name='ping')
    async def ping(self, ctx):
        increment_command_count()
        ms = round(self.bot.latency * 1000)
        embed = discord.Embed(color=WHITE)
        embed.add_field(name="Latency", value=f"{ms}ms", inline=True)
        await ctx.send(embed=embed)

    # ── Help ───────────────────────────────────────────────
    @commands.command(name='help', aliases=['h'])
    async def help_command(self, ctx):
        increment_command_count()
        view  = HelpView()
        embed = view.build_embed("economy")
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(CommandsCog(bot))