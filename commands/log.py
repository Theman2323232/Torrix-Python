import discord
from discord.ext import commands
import aiohttp
import json
import os
from datetime import datetime
import pytz

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")
        self.warningID = await self.getwarningID()  # Load last warning ID

    async def getwarningID(self):
        if not os.path.exists("warnings.json"):
            return 0
        with open("warnings.json", "r")  as f:
            try:
                data= json.load(f)
                if data:
                    return max(item.get("warningID",0) for item in data)
                return 0
            except json.JSONDecodeError:
                return 0

    @commands.command()
    async def log(self, ctx, username: str, *, reason: str):
        mod = ctx.author.name
        modid = ctx.author.id
        await ctx.message.delete()

        user_id = await self.get_user_id(username)
        if not user_id:
            await ctx.send(f"❌ Could not find user `{username}`.", delete_after=5)
            return
        info = await self.get_user_info(user_id)
        self.warningID +=1
        embed = discord.Embed(title="⚠️Warning⚠️", color=discord.Color.dark_green())
        embed.add_field(name="Moderator: ",value=f"{mod} ({modid})",inline= False)
        embed.add_field(name="User:", value=f"{info.get('name')} ({info.get('id')})", inline=True)
        embed.add_field(name="Reason:", value=reason, inline=False)
        cst = pytz.timezone('US/Central')
        now_cst = datetime.now(cst)
        embed.timestamp =  now_cst.astimezone(pytz.utc)
        channel = await self.bot.fetch_channel("1381729409974669322")
        date = now_cst.strftime('%Y-%m-%d %H:%M:%S')
        self.save_warning(info.get('id'), info.get('name'), reason, date, mod, modid, self.warningID)
        await channel.send(embed=embed)
        await ctx.send("✅ Warning logged!")

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

    def save_warning(self, id, username, reason, date, mod, modid, warningID):
        warning = {"id": id,"username": username, "reason": reason, "date": date, "mod": mod, "modid": modid, "warningID": warningID}

        if not os.path.exists("warnings.json"):
            with open("warnings.json", "w") as f:
                json.dump([], f)

        with open("warnings.json", "r") as f:
            data = json.load(f)

        data.append(warning)

        with open("warnings.json", "w") as f:
            json.dump(data, f, indent=4)


async def setup(bot):
    await bot.add_cog(Log(bot))
