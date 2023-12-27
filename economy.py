import discord
from discord.ext import commands
import json
import random
import datetime


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")

    @commands.command()
    async def balance(self, ctx, member: discord.Member=None):
        with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "r", encoding="utf-8") as f:
            user_eco = json.load(f)

        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        if str(member.id) not in user_eco:
            user_eco[str(member.id)] = {}
            user_eco[str(member.id)]['Balance'] = 100
            user_eco[str(member.id)]['Deposited'] = 0

            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)

        eco_embed = discord.Embed(title=f"{member.name}'s current balance", description="The current balance of this user", color=discord.Color.blue())
        eco_embed.add_field(name="Current balance:", value=f"${user_eco[str(member.id)]['Balance']}.")
        eco_embed.add_field(name="Deposited:", value=f"${user_eco[str(member.id)]['Deposited']}")
        eco_embed.set_footer(text="Want to increase your balance? Try running some economy based commands!", icon_url=None)

        await ctx.send(embed=eco_embed)

    @commands.cooldown(1, per=3600)
    @commands.command()
    async def beg(self, ctx):
        with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "r", encoding="utf-8") as f:
            user_eco = json.load(f)


        if str(ctx.author.id) not in user_eco:

            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]['Balance'] = 0
            user_eco[str(ctx.author.id)]['Deposited'] = 0

            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)

        cur_bal = user_eco[str(ctx.author.id)]['Balance']
        amount = random.randint(-10, 30)
        new_bal = cur_bal + amount      

        if cur_bal > new_bal:
            eco_embed = discord.Embed(title="Oh no! - You've been robbed!", description="A group of robbers saw opportunity in taking advantage of you.", color=discord.Color.red())
            eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)  
            eco_embed.set_footer(text="Should probably beg in a nicer part of town...", icon_url=None)
            await ctx.send(embed=eco_embed)

            user_eco[str(ctx.author.id)]['Balance'] += amount

            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)
        elif cur_bal < new_bal:
            eco_embed = discord.Embed(title="Oh sweet green", description="Some kind souls out there have given you what they could", color=discord.Color.green())
            eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)  
            eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!", icon_url=None)
            await ctx.send(embed=eco_embed)

            user_eco[str(ctx.author.id)]['Balance'] += amount

            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)     
        elif cur_bal == new_bal:
            eco_embed = discord.Embed(title="Awh that sucks!", description="Looks like begging didn't get you anywhere today", color=discord.Color.green())
            eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)  
            eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!", icon_url=None)
            await ctx.send(embed=eco_embed)

    @commands.cooldown(1, per=3600)    
    @commands.command()
    async def work(self, ctx):
        with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "r", encoding="utf-8") as f:
            user_eco = json.load(f)


        if str(ctx.author.id) not in user_eco:

            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]['Balance'] = 0
            user_eco[str(ctx.author.id)]['Deposited'] = 0

            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)  


        amount = random.randint(100, 300)
        user_eco[str(ctx.author.id)]['Balance'] += amount

    
        eco_embed = discord.Embed(title="Phew!", description="After a tiring shift, here's what you earned:", color=discord.Color.green())
        eco_embed.add_field(name="Earnings:",value=f"${amount}", inline=False)
        eco_embed.add_field(name="New Balance:", value=f"${user_eco[str(ctx.author.id)]['Balance']}")
        await ctx.send(embed=eco_embed)

        with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
            json.dump(user_eco, f, indent=4)

    @commands.cooldown(1, per=3600)
    @commands.command()
    async def steal(self, ctx, member: discord.Member):
        with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "r", encoding="utf-8") as f:
            user_eco = json.load(f)

        steal_probability = random.randint(0, 1)

        if steal_probability == 1:
            amount = random.randint(50, 350)
            if str(ctx.author.id) not in user_eco:

                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]['Balance'] = 0
                user_eco[str(ctx.author.id)]['Deposited'] = 0


                with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                    json.dump(user_eco, f, indent=4) 
            elif str(member.id) not in user_eco:

                user_eco[str(member.id)] = {}
                user_eco[str(member.id)]['Balance'] = 0

                with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                    json.dump(user_eco, f, indent=4)

            user_eco[str(ctx.author.id)]['Balance'] += amount
            user_eco[str(member.id)]['Balance'] -= amount  
            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)


            steal_embed = discord.Embed(title="Stole Money", description=f"{ctx.author.mention} has stolen from {member.mention}! Be sure to keep it safe as they may be looking for revenge...",color=discord.Color.green())
            steal_embed.add_field(name="Amount:", value=str(amount), inline=False)

            await ctx.send(embed=steal_embed)
        elif steal_probability == 0:
            steal_embed = discord.Embed(title="Uh oh!", value=f"You did not get to steal from {member.mention}, better luck next time!")
            await ctx.send(embed=steal_embed)

    @commands.command()
    async def deposit(self, ctx, amount: int):
        with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "r", encoding="utf-8") as f:
            user_eco = json.load(f)            
        if str(ctx.author.id) not in user_eco:

            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]['Balance'] = 0
            user_eco[str(ctx.author.id)]['Deposited'] = 0

            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)       

        if amount > user_eco[str(ctx.author.id)]['Balance']:
            await ctx.reply("You do not have enough funds to deposit!")
        else:
            user_eco[str(ctx.author.id)]['Deposited'] += amount             
            user_eco[str(ctx.author.id)]['Balance'] -= amount             
            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)
            await ctx.reply(f"Successfuly deposited ${amount} into your bank! This money is now safe and only you can touch it.")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "r", encoding="utf-8") as f:
            user_eco = json.load(f)            
        if str(ctx.author.id) not in user_eco:

            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]['Balance'] = 0
            user_eco[str(ctx.author.id)]['Deposited'] = 0

            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)       

        if amount > user_eco[str(ctx.author.id)]['Deposited']:
            await ctx.reply("You do not have enough funds to withdraw!")
        else:
            user_eco[str(ctx.author.id)]['Deposited'] -= amount             
            user_eco[str(ctx.author.id)]['Balance'] += amount             
            with open("Galaxy Games Bot/cogs/jsonfiles/eco.json", "w", encoding="utf-8") as f:
                json.dump(user_eco, f, indent=4)
            await ctx.reply(f"Successfuly withdrawn ${amount} from your bank!")           

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown, you can use it in {str(datetime.timedelta(seconds=int(error.retry_after)))}")
    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown, you can use it in {str(datetime.timedelta(seconds=int(error.retry_after)))}")
    @steal.error
    async def steal_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown, you can use it in {str(datetime.timedelta(seconds=int(error.retry_after)))}")

async def setup(client):
    await client.add_cog(Economy(client))