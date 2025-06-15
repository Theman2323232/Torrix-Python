import discord
from discord.ext import commands
import requests
import os
import asyncio

class savecogfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    async def pinsafdasfafsadsafafdasfafdag(self, ctx):
        await ctx.send("Pong!")

async def setup(bot):
    await bot.add_cog(savecogfile(bot))