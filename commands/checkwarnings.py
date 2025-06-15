import discord
from discord.ext import commands
import aiohttp
import json
from datetime import datetime
import requests

class checkwarnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    async def warnings (self, ctx, username):
        user_id = await self.get_user_id(username)
        if not user_id:
            await ctx.send(f"❌ Could not find user `{username}`.", delete_after=5)
            return
        info = await self.get_user_info(user_id)
        user_id = info.get('id')

        with open("warnings.json", "r") as f:
            data = json.load(f)
        ammount_of_warnings = 0
        for warning in data:
             if str(warning["id"]) == str(user_id):
                  ammount_of_warnings+=1

        with open("warnings.json", "r") as f:
            data = json.load(f)
        matches = [entry for entry in data if entry["id"] == info.get('id')]
        if not matches:
            await ctx.send("No warning with that ID number")
            return
        ammount_of_warnings = len(matches)
        WarningList = "\n".join(f"- {warning['reason']} ({warning['warningID']})" for warning in matches)
        embed = discord.Embed(title=f"🚨 {username.upper()}'s Warnings", color=discord.Color.gold())     
        embed.add_field(name="Total Warnings: ",value=str(ammount_of_warnings),inline= False)
        embed.add_field(name="Warnings: ", value=WarningList,inline= False)
        api_url = ("https://thumbnails.roblox.com/v1/users/avatar-headshot"f"?userIds={user_id}""&size=180x180""&format=Png""&isCircular=false")
        resp = requests.get(api_url).json()
        avatar_url = resp["data"][0]["imageUrl"]
        embed.set_thumbnail(url=avatar_url)  
        embed.set_footer(text="Torrix Moderation Bot")  
        embed.timestamp = discord.utils.utcnow()  
        await ctx.send(embed=embed)
    
    async def get_user_id(self, username):
            url = "https://users.roblox.com/v1/usernames/users"
            payload = {"usernames": [username], "excludeBannedUsers": False}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    data = await resp.json()
                    if data['data']:
                        return data['data'][0]['id']
            return None
    async def get_user_info(self, user_id):
            url = f"https://users.roblox.com/v1/users/{user_id}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.json()

async def setup(bot):
    await bot.add_cog(checkwarnings(bot))