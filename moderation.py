from typing import List, Optional
import discord
import os
from discord import Member
from discord.components import SelectOption
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions, has_role, MissingRequiredArgument
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

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation commands are ready!")

    @commands.command()
    @commands.has_role("+")
    async def setmuterole(self, ctx, role: discord.Role):
        with open("Galaxy Games Bot/cogs/jsonfiles/mutes.json", "r", encoding="utf-8") as f:
            mute_role = json.load(f)

            mute_role[str(ctx.guild.id)] = role.name
        with open("Galaxy Games Bot/cogs/jsonfiles/mutes.json", "w", encoding="utf-8") as f:
            json.dump(mute_role, f, indent=4)
        
        await ctx.send(f"Mute role has been changed to {role.mention}")

    @commands.command()
    @commands.has_role("Moderation")
    async def mute(self, ctx, member: discord.Member, *, reason):
        with open("Galaxy Games Bot/cogs/jsonfiles/mutes.json", "r", encoding="utf-8") as f:
            role = json.load(f)
            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        role = discord.utils.find(lambda r: r.name == 'Moderation', ctx.message.guild.roles)
        if role in member.roles:
            await ctx.send("Cannot mute this user")
        else:
            await member.add_roles(mute_role)
            await ctx.send(f"{member.mention} has been muted by {ctx.author.mention}")
            conf_embed = discord.Embed(title="Member Muted!", color=discord.Color.blue())
            conf_embed.add_field(name="Muted: ",value=f"{member.mention} ({member.id}) was muted by {ctx.author.mention}", inline=False)
            conf_embed.add_field(name="Reason: ", value=reason, inline=False)
            conf_embed.set_footer(text="This bot was created by RoFishy")


            channel = self.client.get_channel(1138849362638815515)
            
            await channel.send(embed=conf_embed)

    @commands.command()
    @commands.has_role("Moderation")
    async def unmute(self, ctx, member: discord.Member, *, reason):
        with open("Galaxy Games Bot/cogs/jsonfiles/mutes.json", "r", encoding="utf-8") as f:
            role = json.load(f)
            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} has been unmuted by {ctx.author.mention}")
        conf_embed = discord.Embed(title="Member Unmuted!", color=discord.Color.blue())
        conf_embed.add_field(name="Unmuted: ",value=f"{member.mention} ({member.id}) was unmuted by {ctx.author.mention}", inline=False)
        conf_embed.add_field(name="Reason: ", value=reason, inline=False)
        conf_embed.set_footer(text="This bot was created by RoFishy")


        channel = self.client.get_channel(1138849362638815515)
        
        await channel.send(embed=conf_embed)        

    

    @commands.command()
    @commands.has_role("Moderation")
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)

    @commands.command()
    @commands.has_role("Moderation")
    async def kick(self, ctx, member: discord.Member, *, reason):
        role = discord.utils.find(lambda r: r.name == 'Moderation', ctx.message.guild.roles)
        if role in member.roles:
            await ctx.send("Cannot kick this user")
        else:
            await ctx.guild.kick(member)
            await ctx.send(f"{member.mention} has been kicked by {ctx.author.mention}")

            conf_embed = discord.Embed(title="Member Kicked!", color=discord.Color.blue())
            conf_embed.add_field(name="Kicked: ",value=f"{member.mention} ({member.id}) was kicked by {ctx.author.mention}", inline=False)
            conf_embed.add_field(name="Reason: ", value=reason, inline=False)
            conf_embed.set_footer(text="This bot was created by RoFishy")


            channel = self.client.get_channel(1138849362638815515)
            
            await channel.send(embed=conf_embed)
    @commands.command()
    @commands.has_role("Moderation")
    async def ban(self, ctx, member: discord.Member, *, reason):
        
        role = discord.utils.find(lambda r: r.name == 'Moderation', ctx.message.guild.roles)
        if role in member.roles:
            await ctx.send("Cannot ban this user")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"{member.mention} has been banned by {ctx.author.mention}")

            conf_embed = discord.Embed(title="Member Banned!", color=discord.Color.blue())
            conf_embed.add_field(name="Banned: ",value=f"{member.mention} ({member.id}) was banned by {ctx.author.mention}", inline=False)
            conf_embed.add_field(name="Reason: ", value=reason, inline=False)
            conf_embed.set_footer(text="This bot was created by RoFishy")


            channel = self.client.get_channel(1138849362638815515)
            
            await channel.send(embed=conf_embed)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_role("Moderation")
    async def unban(self, ctx, userId, *, reason):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        await ctx.send(f"{userId} has been unbanned by {ctx.author.mention}")

        conf_embed = discord.Embed(title="Member Unbanned!", color=discord.Color.blue())
        conf_embed.add_field(name="Banned: ",value=f"{userId} was unbanned by {ctx.author.mention}", inline=False)
        conf_embed.add_field(name="Reason: ", value=reason, inline=False)
        conf_embed.set_footer(text="This bot was created by RoFishy")


        channel = self.client.get_channel(1138849362638815515)
        
        await channel.send(embed=conf_embed)


    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please enter all required arguments!")
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please enter all required arguments!")
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please enter all required arguments!")
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please enter all required arguments!")
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please enter all required arguments!")




async def setup(client):
    await client.add_cog(Moderation(client))