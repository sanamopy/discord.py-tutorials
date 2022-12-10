import discord
from discord.ext import commands
from discord import app_commands

class cog2(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="cog2", description="Sends hello!")
  async def cog2(self, interaction: discord.Interaction):
    await interaction.response.send_message(content="Hello!")

async def setup(client:commands.Bot) -> None:
  await client.add_cog(cog2(client))