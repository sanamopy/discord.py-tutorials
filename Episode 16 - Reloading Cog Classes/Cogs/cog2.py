from discord.ext import commands
from discord import app_commands
import discord

class cog2(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="hey", description="Sends hey!")
  async def hey(self, interaction: discord.Interaction):
    await interaction.response.send_message("Hey!")

async def setup(client:commands.Bot) -> None:
  await client.add_cog(cog2(client))