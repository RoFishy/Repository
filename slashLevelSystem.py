import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio
import math
import random

class slashLevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        with open("Galaxy Games Bot/cogs/jsonfiles/users.json", "r", encoding="utf-8") as f:
            self.users = json.load(f)


    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashLevelSystem.py is ready")
        await self.client.tree.sync()

    @app_commands.command(name="level", description="Check a users level and experience in the server!")
    async def level(self, interaction: discord.Interaction, user: discord.User=None) :
        if user is None:
            user = interaction.user
        elif user is not None:
            user = user
        
        level_card = discord.Embed(title=f"{user.name}'s Level & Experience", color=discord.Color.blue())
        level_card.add_field(name="Level", value=self.users[str(user.id)]['Level'])
        level_card.add_field(name="Experience", value=self.users[str(user.id)]['Experience'])
        level_card.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
        
        await interaction.response.send_message(embed=level_card)

async def setup(client):
    await client.add_cog(slashLevelSystem(client))