import discord
from discord.ext import commands
import aiohttp
import requests
import json
import os
import asyncio
from discord import app_commands
from commands.shift import MyView
from dotenv import load_dotenv
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True # Enable message content intent


token = os.getenv('MY_SECRET_TOKEN')

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    bot.add_view(MyView())
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey")
    

async def Load():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")

async def main():
    async with bot:
        await Load()

        await bot.start(token)



asyncio.run(main())






















