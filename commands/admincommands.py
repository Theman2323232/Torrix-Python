import discord
from discord.ext import commands
from datetime import datetime
class admincommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
            title="You have been banned!",
            description=f"Reason: {reason}" if reason else "No reason provided.",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Torrix Moderation Bot")
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("Could not DM the user.")
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"<@{user_id}> has been unbanned!")

    

    

async def setup(bot):
    await bot.add_cog(admincommands(bot))