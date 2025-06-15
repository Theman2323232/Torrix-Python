from discord.ext import commands
from services.erlc_api import ERLCAPI
import discord
import asyncio
class ERLCCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    async def igc(self, ctx, *, full_command):
        import requests, json

        # Split first word as command, rest as message
        parts = full_command.split(maxsplit=1)
        if len(parts) < 2:
            await ctx.send("You must provide both a command and a message.")
            return

        command, message = parts[0], parts[1]

        response = requests.post(
            "https://api.policeroleplay.community/v1/server/command",
            headers={
                "server-key": "dCCUzWqbDoQRAVLfeORN-ezGAyrWHTTlXTUbULymimabNhFNeynnBKWpyGFaf",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "command": f":{command} {message}"
            })
        )

        if response.status_code == 200:
            await ctx.send(f"✅ Sent command: :{command} {message}")
        else:
            await ctx.send(f"❌ Failed to send command. Status {response.status_code}: {response.text}")

    @commands.command()
    async def ingame(self, ctx):
        import requests
        import discord

        response = requests.get(
            "https://api.policeroleplay.community/v1/server/players",
            headers={
                "server-key": "dCCUzWqbDoQRAVLfeORN-ezGAyrWHTTlXTUbULymimabNhFNeynnBKWpyGFaf",
                "Accept": "*/*"
            },
        )
        data = response.json()
        names = [entry['Player'].split(":")[0] for entry in data]
        id = [entry['Player'].split(":")[1] for entry in data]
        names_with_links = [f"[{name}](https://www.roblox.com/users/{user_id}/profile)" for name, user_id in zip(names, id)]
        names_column = "\n".join(names_with_links)

        response1 = requests.get(
        "https://api.policeroleplay.community/v1/server",
        headers={"server-key":"dCCUzWqbDoQRAVLfeORN-ezGAyrWHTTlXTUbULymimabNhFNeynnBKWpyGFaf","Accept":"*/*"},
        )
        data2 = response1.json()
        numingame = data2['CurrentPlayers']
        embed = discord.Embed(
            title=f"Ingame: {numingame}",
            description=f'**{names_column}**',
            color=discord.Color.dark_gray()
        )
        await ctx.send(embed=embed)
  
    @commands.command()
    async def ssd(self, ctx):
            
            import requests, json
            response = requests.post(
                "https://api.policeroleplay.community/v1/server/command",
                headers={
                    "server-key": "dCCUzWqbDoQRAVLfeORN-ezGAyrWHTTlXTUbULymimabNhFNeynnBKWpyGFaf",
                    "Content-Type": "application/json"
                },
                data=json.dumps({"command": f":m The server is being shutdown.\nYou will be kicked, this is not a moderation action"})
            )

            await asyncio.sleep(5)

            response = requests.post(
                "https://api.policeroleplay.community/v1/server/command",
                headers={
                    "server-key": "dCCUzWqbDoQRAVLfeORN-ezGAyrWHTTlXTUbULymimabNhFNeynnBKWpyGFaf",
                    "Content-Type": "application/json"
                },
                data=json.dumps({"command": f":kick all"})
            )
            if response.status_code == 200:
                await ctx.send(f"✅ Sent command")
            else:
                await ctx.send(f"❌ Failed to send command. Status {response.status_code}: {response.text}")

    @commands.command()
    async def gamelogs(self, ctx, number: int = 25):
        import requests

        response = requests.get(
            "https://api.policeroleplay.community/v1/server/commandlogs",
            headers={"server-key":"dCCUzWqbDoQRAVLfeORN-ezGAyrWHTTlXTUbULymimabNhFNeynnBKWpyGFaf","Accept":"*/*"},
        )
        data = response.json()
        lines =[]
        for entry in data:
            names = entry['Player'].split(":")[0]
            Command = entry['Command']


            lines.append(f"**{names}** ran `{Command}`")

        description = "\n".join(lines[:number])  # Limit to 25 lines so embed isn't too long




        embed = discord.Embed(
            title="Ingame:",
            description=description,
            color=discord.Color.dark_gray()
        )
        await ctx.send(embed=embed)











async def setup(bot):
    await bot.add_cog(ERLCCommands(bot))
