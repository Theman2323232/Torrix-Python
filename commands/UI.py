import discord
from discord.ext import commands
import requests


class UI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    async def ui(self, ctx, username: str):
        user_id = get_user_id(username)
        if not user_id:
            await ctx.send(f"❌ Could not find user `{username}`.")
            return

        info = get_user_info(user_id)
        
        headshot_url = get_headshot_url(info.get('id'))
        if not headshot_url:
            headshot_url = "https://via.placeholder.com/420?text=No+Avatar"

        embed = discord.Embed()
        embed.set_author(name=info.get('name'), icon_url=headshot_url)
        embed.add_field(name="User ID", value=info.get('id'), inline=False)
        embed.add_field(name="Created", value=info.get('created'), inline=True)
        embed.add_field(name="Description", value=info.get('description', 'No description available'), inline=False)
        await ctx.send(embed=embed)

def get_user_id(username):
        url = "https://users.roblox.com/v1/usernames/users"
        payload = {"usernames": [username], "excludeBannedUsers": False}
        response = requests.post(url, json=payload)
        data = response.json()

        if data['data']:
            return data['data'][0]['id']
        else:
            print("❌ Username not found.")
        return None
    
def get_user_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    return response.json()

def get_headshot_url(user_id):
    url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png"
    response = requests.get(url).json()
    try:
        return response['data'][0]['imageUrl']
    except (KeyError, IndexError):
        return None

async def setup(bot):
    await bot.add_cog(UI(bot))
