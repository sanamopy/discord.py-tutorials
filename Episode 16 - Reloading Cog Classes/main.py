import discord
from discord.ext import commands
import json
from typing import Literal

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='.', intents=discord.Intents().all())
    self.cogslist = ["cog1", "cog2"]

  async def on_ready(self):
    print(" Logged in as " + self.user.name)
    synced = await self.tree.sync()
    print(" Slash CMDs Synced "+ str(len(synced)) + " Commands")

  async def setup_hook(self):
    for ext in self.cogslist:
      await self.load_extension("Cogs."+ext)

with open('config.json', 'r') as f: 
  TOKEN = json.load(f)['TOKEN']

client = Client()

@client.tree.command(name="reload", description="Reloads a Cog Class")
async def reload(interaction: discord.Interaction, cog:Literal["Cog1", "Cog2"]):
  try:
    await client.reload_extension(name="Cogs."+cog.lower())
    await interaction.response.send_message(f"Successfully reloaded **{cog}.py**")
  except Exception as e:
    await interaction.response.send_message(f"Failed! Could not reload this cog class. See error below\n```{e}```")

client.run(TOKEN)
