import discord
from discord.ext import commands
import random
from bank_system import BankSystem
from commands_manager import increment_command_count
import asyncio

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank = BankSystem()
        self.blackjack_games = {}

    @commands.command(name='coinflip', aliases=['cf', 'flip'])
    async def coinflip(self, ctx, amount: int, choice: str = None):
        increment_command_count()
        
        if amount < 10:
            await ctx.send("❌ Minimum bet: $10")
            return
        
        user_data = self.bank.get_user_data(ctx.author.id)
        if user_data['balance'] < amount:
            await ctx.send(f"❌ Not enough money. Balance: ${user_data['balance']:,}")
            return
        
        if choice is None:
            choice = random.choice(['heads', 'tails'])
        
        choice = choice.lower()
        if choice not in ['heads', 'tails', 'h', 't']:
            await ctx.send("❌ Choose `heads` or `tails`")
            return
        
        if choice in ['h', 'heads']:
            choice = 'heads'
        else:
            choice = 'tails'
        
        result = random.choice(['heads', 'tails'])
        
        embed = discord.Embed(title="🪙 Coinflip", color=0xf59e0b)
        embed.add_field(name="Your choice", value=choice.capitalize(), inline=True)
        embed.add_field(name="Result", value=result.capitalize(), inline=True)
        
        if result == choice:
            winnings = amount
            self.bank.add_money(ctx.author.id, winnings)
            embed.color = 0x10b981
            embed.add_field(name="🎉 You won", value=f"+${winnings:,}", inline=False)
        else:
            self.bank.remove_money(ctx.author.id, amount)
            embed.color = 0xef4444
            embed.add_field(name="😢 You lost", value=f"-${amount:,}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='slots', aliases=['slot'])
    async def slots(self, ctx, amount: int):
        increment_command_count()
        
        if amount < 10:
            await ctx.send("❌ Minimum bet: $10")
            return
        
        user_data = self.bank.get_user_data(ctx.author.id)
        if user_data['balance'] < amount:
            await ctx.send(f"❌ Not enough money. Balance: ${user_data['balance']:,}")
            return
        
        self.bank.remove_money(ctx.author.id, amount)
        
        symbols = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣', '⭐']
        weights = [30, 25, 20, 15, 6, 3, 1]
        
        result = random.choices(symbols, weights=weights, k=3)
        
        embed = discord.Embed(title="🎰 Slots", color=0x5865F2)
        embed.add_field(name="Result", value=f"║ {' │ '.join(result)} ║", inline=False)
        
        if result[0] == result[1] == result[2]:
            if result[0] == '7️⃣':
                multiplier = 50
            elif result[0] == '💎':
                multiplier = 25
            elif result[0] == '⭐':
                multiplier = 100
            else:
                multiplier = 10
            
            winnings = amount * multiplier
            self.bank.add_money(ctx.author.id, winnings)
            embed.color = 0x10b981
            embed.add_field(name="🎉 JACKPOT!", value=f"+${winnings:,} (x{multiplier})", inline=False)
        elif result[0] == result[1] or result[1] == result[2]:
            winnings = amount * 2
            self.bank.add_money(ctx.author.id, winnings)
            embed.color = 0xf59e0b
            embed.add_field(name="✨ Double!", value=f"+${winnings:,} (x2)", inline=False)
        else:
            embed.color = 0xef4444
            embed.add_field(name="😢 No luck", value=f"-${amount:,}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='blackjack', aliases=['bj', '21'])
    async def blackjack(self, ctx, amount: int):
        increment_command_count()
        
        if amount < 10:
            await ctx.send("❌ Minimum bet: $10")
            return
        
        user_data = self.bank.get_user_data(ctx.author.id)
        if user_data['balance'] < amount:
            await ctx.send(f"❌ Not enough money.")
            return
        
        if ctx.author.id in self.blackjack_games:
            await ctx.send("❌ You already have an active game. Use `!hit` or `!stand`")
            return
        
        self.bank.remove_money(ctx.author.id, amount)
        
        cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        random.shuffle(cards)
        
        player_hand = [cards.pop(), cards.pop()]
        dealer_hand = [cards.pop(), cards.pop()]
        
        self.blackjack_games[ctx.author.id] = {
            'bet': amount,
            'player': player_hand,
            'dealer': dealer_hand,
            'deck': cards
        }
        
        player_value = self.calculate_hand(player_hand)
        
        embed = discord.Embed(title="🃏 Blackjack", color=0x5865F2)
        embed.add_field(name="Your hand", value=f"{' '.join(player_hand)} = **{player_value}**", inline=False)
        embed.add_field(name="Dealer", value=f"{dealer_hand[0]} | ??", inline=False)
        embed.set_footer(text="Use !hit to draw or !stand to stay")
        
        if player_value == 21:
            await self.end_blackjack(ctx, ctx.author.id, "blackjack")
        else:
            await ctx.send(embed=embed)

    @commands.command(name='hit')
    async def hit(self, ctx):
        if ctx.author.id not in self.blackjack_games:
            await ctx.send("❌ No active game. Use `!blackjack [amount]`")
            return
        
        game = self.blackjack_games[ctx.author.id]
        game['player'].append(game['deck'].pop())
        player_value = self.calculate_hand(game['player'])
        
        embed = discord.Embed(title="🃏 Blackjack", color=0x5865F2)
        embed.add_field(name="Your hand", value=f"{' '.join(game['player'])} = **{player_value}**", inline=False)
        embed.add_field(name="Dealer", value=f"{game['dealer'][0]} | ??", inline=False)
        
        if player_value > 21:
            await self.end_blackjack(ctx, ctx.author.id, "bust")
        elif player_value == 21:
            await self.end_blackjack(ctx, ctx.author.id, "stand")
        else:
            embed.set_footer(text="Use !hit to draw or !stand to stay")
            await ctx.send(embed=embed)

    @commands.command(name='stand')
    async def stand(self, ctx):
        if ctx.author.id not in self.blackjack_games:
            await ctx.send("❌ No active game.")
            return
        
        await self.end_blackjack(ctx, ctx.author.id, "stand")

    async def end_blackjack(self, ctx, user_id, reason):
        game = self.blackjack_games.pop(user_id)
        player_value = self.calculate_hand(game['player'])
        
        while self.calculate_hand(game['dealer']) < 17:
            game['dealer'].append(game['deck'].pop())
        
        dealer_value = self.calculate_hand(game['dealer'])
        
        embed = discord.Embed(title="🃏 Blackjack - Result", color=0x5865F2)
        embed.add_field(name="Your hand", value=f"{' '.join(game['player'])} = **{player_value}**", inline=False)
        embed.add_field(name="Dealer", value=f"{' '.join(game['dealer'])} = **{dealer_value}**", inline=False)
        
        if reason == "bust":
            embed.color = 0xef4444
            embed.add_field(name="😢 Bust!", value=f"-${game['bet']:,}", inline=False)
        elif reason == "blackjack":
            winnings = int(game['bet'] * 2.5)
            self.bank.add_money(user_id, winnings)
            embed.color = 0x10b981
            embed.add_field(name="🎉 BLACKJACK!", value=f"+${winnings:,}", inline=False)
        elif dealer_value > 21:
            winnings = game['bet'] * 2
            self.bank.add_money(user_id, winnings)
            embed.color = 0x10b981
            embed.add_field(name="🎉 Dealer bust!", value=f"+${winnings:,}", inline=False)
        elif player_value > dealer_value:
            winnings = game['bet'] * 2
            self.bank.add_money(user_id, winnings)
            embed.color = 0x10b981
            embed.add_field(name="🎉 You won!", value=f"+${winnings:,}", inline=False)
        elif player_value < dealer_value:
            embed.color = 0xef4444
            embed.add_field(name="😢 You lost", value=f"-${game['bet']:,}", inline=False)
        else:
            self.bank.add_money(user_id, game['bet'])
            embed.color = 0xf59e0b
            embed.add_field(name="🤝 Tie", value="Bet returned", inline=False)
        
        await ctx.send(embed=embed)

    def calculate_hand(self, hand):
        value = 0
        aces = 0
        
        for card in hand:
            if card in ['J', 'Q', 'K']:
                value += 10
            elif card == 'A':
                aces += 1
                value += 11
            else:
                value += int(card)
        
        while value > 21 and aces:
            value -= 10
            aces -= 1
        
        return value

    @commands.command(name='roulette', aliases=['roul'])
    async def roulette(self, ctx, amount: int, bet: str):
        increment_command_count()
        
        if amount < 10:
            await ctx.send("❌ Minimum bet: $10")
            return
        
        user_data = self.bank.get_user_data(ctx.author.id)
        if user_data['balance'] < amount:
            await ctx.send("❌ Not enough money.")
            return
        
        self.bank.remove_money(ctx.author.id, amount)
        
        result = random.randint(0, 36)
        
        red_nums = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        if result == 0:
            color = 'green'
            emoji = '🟢'
        elif result in red_nums:
            color = 'red'
            emoji = '🔴'
        else:
            color = 'black'
            emoji = '⚫'
        
        embed = discord.Embed(title="🎡 Roulette", color=0x5865F2)
        embed.add_field(name="Result", value=f"{emoji} **{result}** ({color})", inline=False)
        
        bet = bet.lower()
        won = False
        multiplier = 0
        
        if bet in ['red', 'r']:
            won = color == 'red'
            multiplier = 2
        elif bet in ['black', 'b']:
            won = color == 'black'
            multiplier = 2
        elif bet in ['green', 'g', '0']:
            won = result == 0
            multiplier = 35
        elif bet.isdigit() and 0 <= int(bet) <= 36:
            won = result == int(bet)
            multiplier = 35
        else:
            self.bank.add_money(ctx.author.id, amount)
            await ctx.send("❌ Invalid bet. Use: red, black, green, or a number 0-36")
            return
        
        if won:
            winnings = amount * multiplier
            self.bank.add_money(ctx.author.id, winnings)
            embed.color = 0x10b981
            embed.add_field(name="🎉 You won!", value=f"+${winnings:,} (x{multiplier})", inline=False)
        else:
            embed.color = 0xef4444
            embed.add_field(name="😢 You lost", value=f"-${amount:,}", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GamesCog(bot))
