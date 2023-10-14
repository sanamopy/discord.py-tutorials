import discord
from discord.ext import commands
from discord import app_commands
import json

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='.', intents=discord.Intents().all())

  async def on_ready(self):
    print(" Logged in as " + self.user.name)
    synced = await self.tree.sync()
    print(" Slash CMDs Synced "+ str(len(synced)) + " Commands")

with open('config.json', 'r') as f: 
  TOKEN = json.load(f)['TOKEN']

client = Client()

#
# Custom check created by the user
# Can edit this however you'd like, but there must be a return True and return False
#
def my_check(interaction: discord.Interaction):
  if interaction.user.top_role.name=="Admin":
    return True
  return False

#
# Command used for testing
#
@client.tree.command(name="test")
@app_commands.checks.bot_has_permissions(administrator=True) # Will return True if bot has Administrator perms (Accepts any permission & can be True/False)
@app_commands.checks.has_permissions(administrator=True) # Will return True if user has Administator perms (Accepts any permission & can be True/False)
@app_commands.checks.has_role("Admin") # Will return True if user has a role by the name of Admin (Accepts role names or IDs)
@app_commands.checks.has_any_role([918333581758193694, 680584954136100890, 680586241787691021]) # Will return True if the user has any of the roles with the IDs listed (Accepts role names or IDs)
@app_commands.checks.cooldown(1, 5.0) # Can only run the command once every 5.0 seconds. For hours, minutes, days, etc, just convert to seconds
@app_commands.check(my_check) # Will only return True if the my_check function returns True
async def test(interaction: discord.Interaction):
  await interaction.response.send_message("Worked") # This will only run if all of the checks above pass

#
# Error handler
#
@test.error
async def test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
  if isinstance(error, discord.app_commands.CommandOnCooldown):
    await interaction.response.send_message(content=f"Failed! You can only run this command 3 times every 15 seconds. {str(error)}", ephemeral=True)
  elif isinstance(error, discord.app_commands.MissingPermissions):
    await interaction.response.send_message(content=f"Failed! You don't have the proper permissions. {str(error)}", ephemeral=True)
  else:
    await interaction.response.send_message(content={str(error)}, ephemeral=True)

client.run(TOKEN)
