from discord.ext import commands
from typing import Literal
import discord
import json

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='.', intents=discord.Intents().all())
    self.cogslist = ['Cogs.tickets']

  async def on_ready(self):
    print(" Logged in as " + self.user.name)
    synced = await self.tree.sync()
    print(" Slash CMDs Synced "+ str(len(synced)) + " Commands")

  async def setup_hook(self):
    for ext in self.cogslist:
      await self.load_extension(ext)

with open('config.json', 'r') as f: 
  TOKEN = json.load(f)['TOKEN']

client = Client()

@client.tree.command(name="reload", description="Reloads a Cog Class")
async def reload(interaction: discord.Interaction, cog:Literal["Tickets"]):
    await client.reload_extension(f"Cogs.{cog.lower()}")
    await interaction.response.send_message(f"Successfully reloaded **{cog}.py**", ephemeral=True) 

client.run(TOKEN)
