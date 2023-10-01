from discord.ext import commands
from discord import app_commands
import discord

class cog1(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="hello", description="Sends hello!")
  async def hello(self, interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")f

async def setup(client:commands.Bot) -> None:
  await client.add_cog(cog1(client))