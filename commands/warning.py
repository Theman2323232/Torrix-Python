import discord
from discord.ext import commands
import json

class warning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    async def warning (self, ctx, number: int):
       
        with open("warnings.json", "r") as f:
            data = json.load(f)
        matches = [entry for entry in data if entry["warningID"] == number]
        if not matches:
            await ctx.send("No warning with that ID number")
            return
        for warning in matches:
            embed = discord.Embed(title=f"⚠️Warning #{number}⚠️", color=discord.Color.dark_blue())
            embed.add_field(name="Moderator: ",value=f"<@{warning['modid']}> ({warning['modid']})",inline= False)
            embed.add_field(name="Accused: ",value=f"{warning['username']} ({warning['id']})",inline= False)
            embed.add_field(name="Reason: ",value=f"{warning['reason']}",inline= False)
            embed.add_field(name="Date and Time: ",value=f"{warning['date']}",inline= False)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(warning(bot))