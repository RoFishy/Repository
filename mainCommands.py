from typing import List, Optional
import discord
import os
from discord import Member
from discord.components import SelectOption
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions, has_role
from itertools import cycle
import random
import json
import aiohttp
import base64
import time
from io import BytesIO
from PIL import Image
from discord.utils import MISSING
import uuid
import requests
import openai

class Main(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("main commands are ready!")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Galaxy Games | !help"))

    @commands.command()
    async def ping(self, ctx):
        bot_latency = round(self.client.latency * 1000)
        await ctx.reply(f"Pong! The bot's latency is {bot_latency}ms")

    @commands.command("8ball")
    async def magic_eightball(self, ctx, *, question):
        with open("Galaxy Games Bot/responses.txt", "r", encoding='utf-8') as f:
            random_responses = f.readlines()
            response = random.choice(random_responses)
            await ctx.reply(response)

    @commands.command()
    async def help(self, ctx):
        help = discord.Embed(title="Commands List",color=discord.Color.blue())
        help.add_field(name="Main Commands", value="!8ball AKA /8ball (question) -- You can ask a question and it will give you a random response!\n!ping AKA /ping-- Check the latency of the bot!\n!chat AKA /chat - IN DEVELOPMENT", inline=False)
        help.add_field(name="Moderation Commands", value="!clear (amount) -- Clears a certain amount of messages\n!kick (user, reason) -- Kicks a user\n!ban (user, reason) -- bans the specified user\n!unban (userID, reason) -- Unbans the specified user\n!mute (user, reason) -- mutes the specified user\n!unmute (user, reason) -- Unmutes the specified user", inline=False)
        help.set_footer(text="This bot was created by RoFishy")

        await ctx.send(embed=help)
    @commands.command()
    async def chat(self, ctx, *, message):
        '''
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message,
            max_tokens=50,  # You can adjust this as needed
        )

        # Send the response back to the Discord channel
        await ctx.send(response.choices[0].text)
        '''
        await ctx.reply("This command is currently under development")

async def setup(client):
    await client.add_cog(Main(client))
