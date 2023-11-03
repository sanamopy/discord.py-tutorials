from discord import app_commands
from discord.ext import commands
from discord import ui
import discord

class tickets(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="sendtickets", description="Sends the ticket prompt message")
    async def sendtickets(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.greyple(), description="Please select your ticket category down below. Thank you!")
        await interaction.response.send_message("Successfully sent ticket message!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=DropDown())

class DropDown(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
  
    async def create_ticket(self):
        # Get the Ticket "Description"
        # Create the overwrites
        # Make the channel
        # Send/Delete tag 
        # Respond to the user
        # Send the ticket message in the ticket

    @discord.ui.select(options= [discord.SelectOption(label="General Support", emoji="🎟️"),
                                 discord.SelectOption(label="Bug Support", emoji="🐛"),
                                 discord.SelectOption(label="Staff Application", emoji="🗒️")], 
                        placeholder="Select a ticket category...", 
                        custom_id="dropdown")
    async def selectmenu(self, interaction: discord.Interaction, select: ui.select):
        await interaction.response.defer()
        # 
        #

class EnterInfo(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
  
    @discord.ui.button(label="Enter Information", style=discord.ButtonStyle.grey, custom_id="enter_information_button")
    async def enterInfoButton(self, interaction: discord.Interaction, Button: discord.ui.Button):
        pass
        # Send Modal

class PopUp(ui.Modal):
    def __init__(self) -> None:
        super().__init__(timeout=None, title="Title", custom_id="Modal")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        # Place information in embed
        # Edit the channel permissions (allow member to send msgs)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(tickets(client))
