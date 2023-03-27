import discord
from discord.ext import commands
from colorama import Fore
import json

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='.', intents=discord.Intents().all())

  async def on_ready(self):
    print(" Logged in as " + Fore.RED + self.user.name + Fore.RESET)
    synced = await self.tree.sync()
    print(" Slash CMDs Synced " + Fore.RED + str(len(synced)) + " Commands" + Fore.RESET)

with open('config.json', 'r') as f: 
  TOKEN = json.load(f)['TOKEN']

class Buttons(discord.ui.View):
  def __init__(self) -> None:
    super().__init__(timeout=None)
    self.expression = ""
  
  async def add(self, interaction: discord.Interaction, symbol):
    if self.expression == "Cleared!":
      self.expression =""
    self.expression += symbol
    await self.update(interaction)

  async def update(self, interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.message.edit(content=f"```{self.expression}```")

  async def solve(self, interaction: discord.Interaction):
    pi = 3.14159
    try:
      self.expression = str(eval(self.expression))
    except:
      await interaction.response.send_message("This expression is invalid", ephemeral=True)
    await self.update(interaction)
    self.expression = ""

  async def cleared(self, interaction: discord.Interaction):
    self.expression = "Cleared!"
    await self.update(interaction)

  @discord.ui.button(label="clear", style=discord.ButtonStyle.red, row=0)
  async def clear(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.cleared(interaction)

  @discord.ui.button(label="(", style=discord.ButtonStyle.blurple, row=0)
  async def p1(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "(")

  @discord.ui.button(label=")", style=discord.ButtonStyle.blurple, row=0)
  async def p2(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, ")")

  @discord.ui.button(label="/", style=discord.ButtonStyle.blurple, row=0)
  async def divide(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "/")

  @discord.ui.button(label="7", style=discord.ButtonStyle.grey, row=1)
  async def s7(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "7")

  @discord.ui.button(label="8", style=discord.ButtonStyle.grey, row=1)
  async def s8(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "8")

  @discord.ui.button(label="9", style=discord.ButtonStyle.grey, row=1)
  async def s9(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "9")

  @discord.ui.button(label="x", style=discord.ButtonStyle.blurple, row=1)
  async def multi(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "*")

  @discord.ui.button(label="4", style=discord.ButtonStyle.grey, row=2)
  async def s4(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "4")

  @discord.ui.button(label="5", style=discord.ButtonStyle.grey, row=2)
  async def s5(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "5")

  @discord.ui.button(label="6", style=discord.ButtonStyle.grey, row=2)
  async def s6(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "6")

  @discord.ui.button(label="-", style=discord.ButtonStyle.blurple, row=2)
  async def minus(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "-")

  @discord.ui.button(label="1", style=discord.ButtonStyle.grey, row=3)
  async def s1(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "1")

  @discord.ui.button(label="2", style=discord.ButtonStyle.grey, row=3)
  async def s2(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "2")

  @discord.ui.button(label="3", style=discord.ButtonStyle.grey, row=3)
  async def s3(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "3")

  @discord.ui.button(label="+", style=discord.ButtonStyle.blurple, row=3)
  async def plus(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "+")

  @discord.ui.button(label=".", style=discord.ButtonStyle.grey, row=4)
  async def decimal(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, ".")

  @discord.ui.button(label="0", style=discord.ButtonStyle.grey, row=4)
  async def s0(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "0")

  @discord.ui.button(label="π", style=discord.ButtonStyle.grey, row=4)
  async def pi(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.add(interaction, "pi")
  
  @discord.ui.button(label="=", style=discord.ButtonStyle.green, row=4)
  async def equals(self, interaction: discord.Interaction, Button: discord.ui.Button):
    await self.solve(interaction)

client = Client()

@client.tree.command(name="calculator", description="Sends an interactive calculator")
async def calculator(interaction: discord.Interaction):
  await interaction.response.send_message("```Begin Calculating```", view=Buttons())

client.run(TOKEN)
