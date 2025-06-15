import discord
from discord.ext import commands
import requests
import os
import asyncio
import json
class activeshiftsshifttime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    async def activeshifts(self, ctx):
        with open('activeshifts.json', 'r') as f:
            data = json.load(f)
        onshiftlift = []

        for entry in data:
            if 'id' in entry:
                onshiftlift.append(f"<@{entry['id']}>")
        if len(onshiftlift) == 0:
            od = "No one is on shift"
        else:
            od = "\n".join(onshiftlift)
        embed = discord.Embed(
                title="Active Shifts",
                description=f"{od}",
                color=discord.Color.dark_red()
            )

        await ctx.send(embed=embed)







    @commands.command()
    async def shifttime(self, ctx):
        with open('shifttime.json', 'r') as f:
            data = json.load(f)
        await ctx.send(file=discord.File('shifttime.json'))
async def setup(bot):
    await bot.add_cog(activeshiftsshifttime(bot))