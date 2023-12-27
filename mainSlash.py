import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_role
import random
import uuid
import requests
import time
import json
import openai

class mainSlash(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="ping", description="Shows the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f"Pong! The bot's latency is {bot_latency}ms")
        
    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question!")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        with open("Galaxy Games Bot/responses.txt", "r", encoding='utf-8') as f:
            random_responses = f.readlines()
            response = random.choice(random_responses)
            await interaction.response.send_message(response)

    @app_commands.command(name="help", description="Displays a list of commands for the bot")
    async def help(self, interaction:discord.Interaction):
        help = discord.Embed(title="Commands List",color=discord.Color.blue())
        help.add_field(name="Main Commands", value="!8ball AKA /8ball (question) -- You can ask a question and it will give you a random response!\n!ping AKA /ping-- Check the latency of the bot!\n!talk AKA /ask-ai or /talk -- Talk to an AI chatbot!", inline=False)
        help.add_field(name="Moderation Commands", value="!clear (amount) -- Clears a certain amount of messages\n!kick (user, reason) -- Kicks a user\n!ban (user, reason) -- bans the specified user\n!unban (userID, reason) -- Unbans the specified user\n!mute (user, reason) -- mutes the specified user\n!unmute (user, reason) -- Unmutes the specified user", inline=False)
        help.set_footer(text="This bot was created by RoFishy")
        await interaction.response.send_message(embed=help)

    @app_commands.command(name="chat", description="Ask the AI chat bot a question!")
    async def talk(self, interaction: discord.Interaction, message: str):
        # Generate a response from ChatGPT
        '''
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message,
            max_tokens=50,  # You can adjust this as needed
        )

        # Send the response back to the Discord channel
        await interaction.followup.send(response.choices[0].text)
        '''
        await interaction.response.send_message("This command is currently under development")
async def setup(client):
    await client.add_cog(mainSlash(client))