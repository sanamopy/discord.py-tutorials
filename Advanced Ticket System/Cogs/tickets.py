from discord import app_commands
from discord.ext import commands
from discord import ui
import datetime
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
  
    async def create_ticket(self, interaction: discord.Interaction, selection: str):
        # Get the Ticket "Description"
        ticket_descriptions = {"General Support": "Our staff team will be with you shortly!",
                               "Bug Support": "Please do not abuse this bug!",
                               "Staff Application": "Requirements:\n1. Req 1\n2. Req 2\n3. Req3"}
        selected_description = ticket_descriptions.get(selection, "")
        # Create the overwrites
        staff_team = discord.utils.get(interaction.guild.roles, name="Staff Team")
        channel_overwrites = {interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=False),
                              staff_team: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                              interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
        # Make the channel
        number = "0001"
        category = discord.utils.get(interaction.guild.channels, name=selection)
        channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-{number}", overwrites=channel_overwrites, category=category)
        # Send/Delete tag 
        tag = await channel.send(staff_team.mention)
        await tag.delete()
        # Respond to the user
        await interaction.followup.send(content=f"Successfully created your ticket! {channel.mention}", ephemeral=True)
        # Send the ticket message in the ticket
        embed = discord.Embed(description=f"Hey {interaction.user.mention}!\n \n"
                                          ""
                                          f"You have created a new ticket\n"
                                          f"**Type:** {selection}\n \n"
                                          ""
                                          f"{selected_description}\n", color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
        await channel.send(embed=embed, view=EnterInfo(str(selection)))

    @discord.ui.select(options= [discord.SelectOption(label="General Support", emoji="🎟️"),
                                 discord.SelectOption(label="Bug Support", emoji="🐛"),
                                 discord.SelectOption(label="Staff Application", emoji="🗒️")], 
                        placeholder="Select a ticket category...", 
                        custom_id="dropdown")
    async def selectmenu(self, interaction: discord.Interaction, select: ui.select):
        await interaction.response.defer()
        await interaction.message.edit(view=DropDown())
        await self.create_ticket(interaction, select.values[0])

class EnterInfo(discord.ui.View):
    def __init__(self, ticket_type: str) -> None:
        self.ticket_type = ticket_type
        super().__init__(timeout=None)
  
    @discord.ui.button(label="Enter Information", style=discord.ButtonStyle.grey, custom_id="enter_information_button")
    async def enterInfoButton(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.send_modal(PopUp(self.ticket_type))

class PopUp(ui.Modal):
    def __init__(self, ticket_type: str) -> None:
        self.ticket_type = ticket_type
        super().__init__(timeout=None, title=self.ticket_type, custom_id="Modal")

        self.add_item(ui.TextInput(label="What is your name?", placeholder="My name is...", style=discord.TextStyle.short))
        if self.ticket_type == "General Support":
            self.add_item(ui.TextInput(label="What is your issue?", placeholder="My issue is...", style=discord.TextStyle.long))
            self.add_item(ui.TextInput(label="When did you first have this issue?", placeholder="I've been having this issue since...", style=discord.TextStyle.short))
        
        elif self.ticket_type == "Bug Support":
            self.add_item(ui.TextInput(label="Please explain the bug in detail...", placeholder="Include video evidence...", style=discord.TextStyle.long))
        
        elif self.ticket_type == "Staff Application":
            self.add_item(ui.TextInput(label="What are your past experiences?", placeholder="My experiences are...", style=discord.TextStyle.short))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        # Place information in embed
        embed = interaction.message.embeds[0]
        description = embed.description
        
        split_description = description.split("\n \n")

        for item in reversed(self.children):
            split_description.insert(2, f"**{item.label}**\n{item.value}")
        
        embed.description = "\n \n".join(split_description)

        await interaction.message.edit(view=None, embed=embed)
        # Edit the channel permissions (allow member to send msgs)
        permissions = interaction.channel.overwrites_for(interaction.user)
        permissions.send_messages = True
        await interaction.channel.set_permissions(target=interaction.user, overwrite=permissions)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(tickets(client))
