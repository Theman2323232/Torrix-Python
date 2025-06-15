from discord.ext import commands

class purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int): 
        await ctx.channel.purge(limit = number +1)
            

async def setup(bot):
    await bot.add_cog(purge(bot))