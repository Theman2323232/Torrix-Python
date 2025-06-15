import discord
from discord.ext import commands
from discord import ui
import json
import os
from datetime import datetime

class MyView(ui.View):
        def __init__(self,cog):
            super().__init__(timeout=None)
            self.cog = cog

        @ui.button(label="Shift Start", style=discord.ButtonStyle.primary, custom_id="12312321")
        async def button1(self, interaction: discord.Interaction, button: ui.Button):
            user_id = interaction.user.id
            username = interaction.user.name
            current_datetime = datetime.now()
            time_date =  current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            await self.cog.clockin(user_id, username, time_date, interaction)
        @ui.button(label="Shift End", style=discord.ButtonStyle.primary,custom_id="234984939")
        async def button2(self, interaction: discord.Interaction, button: ui.Button):
            username = interaction.user.name
            user_id = interaction.user.id
            await self.cog.clockout(username,user_id, interaction)

class shift(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_view(MyView(self))  # add view on cog load


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ {__name__}")

    

    @commands.command()
    async def sendhub(self,ctx):
        await ctx.channel.purge(limit = 1)
        embed = discord.Embed(
                title="Moderation Hub",
                description="Place Holder",
                color=discord.Color.dark_gray()
            )
        channel = await self.bot.fetch_channel("1382452675815145662")
        await channel.send(embed=embed, view=MyView(self))
    
    

    async def clockin(self, user_id, username, time_date, interaction):
        clocking = {"id": user_id, "username": username, "TaD": time_date}
        if not os.path.exists("activeshifts.json"):
            print("File not found — creating one.")
            with open("activeshifts.json", "w") as f:
                json.dump([], f)
        with open("activeshifts.json", "r") as f:
            data = json.load(f)
        if any(shift["id"] == user_id for shift in data):
            await interaction.response.send_message("You are already clocked in!", ephemeral=True)
        else:
            data.append(clocking)
            with open("activeshifts.json", "w") as f:
                json.dump(data, f, indent=4)

            embed = discord.Embed(
                title="Clocked in!",
                description=f"You clocked in at {time_date}",
                color=discord.Color.dark_green()
            )
            await interaction.response.send_message(embed=embed, ephemeral = True)

            await self.add_on_duty_role(user_id)

    async def clockout(self, username, user_id,interaction):
        if not os.path.exists("activeshifts.json"):
            return False  

        with open("activeshifts.json", "r") as f:
            data = json.load(f)

        user_time = None

        for entry in data:
            if entry['id'] == user_id:
                user_time = entry
                break
        if user_time:
            TaD = user_time["TaD"]
        else:
            TaD = None

        data = [entry for entry in data if not (entry["id"] == user_id)]
        with open("activeshifts.json", "w") as f:
            json.dump(data, f, indent=4)
       
        await self.remove_on_duty_role(user_id)
        delta = await self.loadshifttime(TaD)
  

        embed = discord.Embed(
            title="Clocked out!",
            description=f"You clocked out at {TaD}\n You were clocked in for **{delta}**",
            color=discord.Color.dark_green()
            )
        await interaction.response.send_message(embed=embed, ephemeral = True)
        await self.loggingshifttime(username, user_id, TaD)

        
        

    async def add_on_duty_role(self, user_id):
            guild = self.bot.get_guild(1191567627768823868)  # use int ID
            if not guild:
                return
            user = guild.get_member(user_id)
            if not user:
                return
            role = role = guild.get_role(1382505857706627114)

            if role and role not in user.roles:
                await user.add_roles(role)

    async def remove_on_duty_role(self, user_id):
            guild = self.bot.get_guild(1191567627768823868)
            if not guild:
                return
            user = guild.get_member(user_id)
            if not user:
                return
            role =role = guild.get_role(1382505857706627114)

            if role and role in user.roles:
                await user.remove_roles(role)

    async def loadshifttime(self, TaD):
        current_TaD = datetime.now()
        time_date =  current_TaD.strftime("%Y-%m-%d %H:%M:%S")
        format = "%Y-%m-%d %H:%M:%S"
        clock_in_time = datetime.strptime(TaD, format)
        clock_out_time = datetime.strptime(time_date, format)
        delta = clock_out_time - clock_in_time
        return delta
    
    async def loggingshifttime(self, username, user_id, TaD):
        if not os.path.exists("shifttime.json"):
            print("File not found — creating one.")
            with open("shifttime.json", "w") as f:
                json.dump([], f)

        delta = await self.loadshifttime(TaD)
        print(f"{delta}")

        with open ("shifttime.json" ,"r") as (f):
            data = json.load(f)
        user_time = None
        delta_seconds = (await self.loadshifttime(TaD)).total_seconds()
        for entry in data:
            if entry['id'] == user_id:
                user_time = entry
                break
        if user_time:

            user_time["Total Time"] += delta_seconds
        else:        
            modshift = {"Username": username,"id": user_id,"Total Time": delta_seconds}
            data.append(modshift)

        with open ("shifttime.json" ,"w") as (f):
            json.dump(data, f, indent=4)
            

    
        








    
    

async def setup(bot):
    await bot.add_cog(shift(bot))
