from discord import app_commands
from discord.ext import commands
from discord import ui
from discord.interactions import Interaction
from discord.ui import select
import discord

class tickets(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="sendtickets", description="Sends the ticket prompt message")
  async def sendtickets(self, interaction: discord.Interaction):
    embed = discord.Embed(color=discord.Color.greyple(), description="Please select your ticket category down below that best suits your needs. If you don't see a ticket category that fits your needs, then please select General Support. Our staff team will be with your shortly. Thank you!")
    await interaction.response.send_message("Successfully sent ticket message!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=DropDown())

class DropDown(discord.ui.View):
  def __init__(self) -> None:
    super().__init__(timeout=None)
  
  async def create_ticket(self, interaction: discord.Interaction, category: str):
    staff = discord.utils.get(interaction.guild.roles, name="Staff Team")
    ticket_descriptions = {
      "General Support": {"description": "Please be as descriptive as possible with your issues."},
       "Bug Report": {"description": "Depending on the severity of the bug, you may be eligable for a reward."},
       "Staff Application": {"description": "**Staff Requirements:**\n- Requirement 1...\n- Requirement 2...\n-Requirement 3..."}
    }
    description = ticket_descriptions.get(category, {"description": ""})
    category = discord.utils.get(interaction.guild.categories, name=category)
    overwrites = {
      interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
      interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=False),
      staff: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }
    ticket_number = "0001"
    ticket = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-{ticket_number}", overwrites=overwrites, category=category)
    tag = await ticket.send(staff.mention)
    await tag.delete()
    embed = discord.Embed(description=f"Success! Your ticket has been created {ticket.mention}!", color=discord.Color.greyple())
    await interaction.followup.send(embed=embed, ephemeral=True)
    desc = f"Hey {interaction.user.mention}\n \nYou have made a new ticket!\n**Type:** {category.name}\n \n{description['description']}\n \n**One of our staff members will be with you shortly.**"
    ticket_embed = discord.Embed(description=desc, color=discord.Color.greyple())
    await ticket.send(embed=ticket_embed, view=EnterInfo(category))

  @discord.ui.select(options= [discord.SelectOption(label="General Support", emoji="🎟️"),
                               discord.SelectOption(label="Bug Support", emoji="🐛"),
                               discord.SelectOption(label="Staff Application", emoji="🗒️")], placeholder="Select a ticket category...", custom_id="dropdown")
  async def selectmenu(self, interaction: discord.Interaction, select: select):
    await interaction.response.defer()
    await interaction.message.edit(view=self)
    await self.create_ticket(interaction, select.values[0])

class Empty(discord.ui.View):
  def __init__(self) -> None:
    super().__init__(timeout=None)

class EnterInfo(discord.ui.View):
  def __init__(self, ticket_type) -> None:
    super().__init__(timeout=None)
    self.ticket_type = ticket_type
  
  @discord.ui.button(label="Enter Information", style=discord.ButtonStyle.grey, custom_id="enter_information_button")
  async def enterInfoButton(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await interaction.response.send_modal(PopUp(str(self.ticket_type)))

class PopUp(ui.Modal):
  def __init__(self, ticket_type) -> None:
    self.ticket_type = ticket_type
    self.custom_id = "popup_modal"
    super().__init__(title=self.ticket_type, timeout=None)
    if self.ticket_type=="General Support":
      self.add_item(ui.TextInput(label="What is your name?", placeholder="My name is...", custom_id="name_field_1"))
      self.add_item(ui.TextInput(label="What is your problem?", placeholder="My problem is...", style=discord.TextStyle.long, custom_id="problem_field"))
      self.add_item(ui.TextInput(label="When did this issue start?", placeholder="My name is...", custom_id="start_field"))
    elif self.ticket_type=="Bug Report":
      self.add_item(ui.TextInput(label="What is your name?", placeholder="My name is...", custom_id="name_field_2"))
      self.add_item(ui.TextInput(label="Please explain the bug fully", placeholder="This is the bug...", style=discord.TextStyle.long, custom_id="explain_field"))
      self.add_item(ui.TextInput(label="Video evidence of the bug", placeholder="https://youtube.com...", custom_id="video_field"))
    elif self.ticket_type=="Staff Application":
      self.add_item(ui.TextInput(label="What is your name?", placeholder="My name is...", custom_id="name_field_3"))
      self.add_item(ui.TextInput(label="What role are you applying for?", placeholder="I am applying for this role...", style=discord.TextStyle.long, custom_id="role_field"))
      self.add_item(ui.TextInput(label="How do you stand out?", placeholder="I stand out because...", custom_id="stand_out_field"))

  async def on_submit(self, interaction: Interaction) -> None:
    await interaction.response.defer()

    embed = interaction.message.embeds[0]
    split_description = embed.description.split("\n \n")
    new_description = f"{split_description[0]}\n \n{split_description[1]}\n \n"

    for item in self.children:
      new_description += f"**{item.label}** \n{item.value}\n \n"
    
    del split_description[0]
    del split_description[0]

    new_description += "\n \n".join(split_description)

    embed.description = new_description
    await interaction.message.edit(embed=embed, view=Empty())

    permissions = interaction.channel.overwrites_for(interaction.user)
    permissions.send_messages = True
    await interaction.channel.set_permissions(interaction.user, overwrite=permissions)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(tickets(client))
