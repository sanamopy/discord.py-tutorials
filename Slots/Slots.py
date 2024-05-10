from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord
import asyncio
import random

# NOTE: This file only works under the assumption that you are importing the functions/classes listed below. It will not work without them below, and they are not public
from Assets.functions import get_data, execute, LevelingManager
# All emojis in this file are from the server itself, and need to be replaced with your own emojis
# The function get_data() gets various data required at different places in this file

class Slots(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.data = get_data()

    @app_commands.command(name="slots", description="Starts a game of slots")
    @app_commands.describe(wager="The amount of Zoid Tokens to wager", emojis = "The amount of different emojis in a 5x3 board")
    async def slots(self, interaction: discord.Interaction, wager: str, emojis: Literal[2, 3, 4]):
        if interaction.guild is None:
            return await interaction.response.send_message(content="Commands cannot be ran in DMs!", ephemeral=True)
        if not wager.isnumeric() or not 0.0 < int(wager) < self.data['MAX_BET'] + .1:
            return await interaction.response.send_message(content = f"❌ Failed! Please enter a numeric value between `0` and `{self.data['MAX_BET']}` for your wager!", ephemeral=True)
        wager = int(wager)
        rows = await execute(f"SELECT * FROM `zoid_leveling` WHERE `user_ID` = '{str(interaction.user.id)}'")
        if int(rows[0]['xp']) < wager:
            return await interaction.response.send_message(content = "❌ Failed! You do not have enough Zoid Tokens to wager!", ephemeral = True)
        embed = discord.Embed(title = "Start Game?",
                              color = discord.Color.from_str(self.data['EMBED_COLOR']))
        embed.add_field(name = "Wager", value = f"{wager} Zoid Tokens")
        embed.add_field(name = "Emojis", value = emojis)
        embed.add_field(name = "Game", value = "Slots")
        embed.set_footer(text = "Match 3 slots to win!")
        await interaction.response.send_message(embed = embed, view = ConfirmGame(interaction, wager, emojis))

    @slots.error
    async def slots_error(self, interaction: discord.Interaction, error):
        await interaction.followup.send(content=error, ephemeral=True) if interaction.response.is_done() else await interaction.response.send_message(content=error, ephemeral=True)
  

class ConfirmGame(discord.ui.View):
    def __init__(self, interaction, wager, emojis) -> None:
        self.interaction : discord.Interaction = interaction
        self.wager : int = wager
        self.emojis : int = emojis
        super().__init__(timeout = None)
        self.data = get_data()
    
    @discord.ui.button(label = "Confirm Bet", custom_id = "confirm_bet", style = discord.ButtonStyle.green, row = 0, disabled = False)
    async def confirm_bet(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user != self.interaction.user:
            return await interaction.response.defer()
        await interaction.response.defer()
        lvl_mng = LevelingManager(interaction.user, interaction.channel, -self.wager)
        await lvl_mng.update()
        embed = discord.Embed(title = "Slots Game",
                              description = "Spin the slot by clicking on the *Spin* button!",
                              color = discord.Color.from_str(self.data['EMBED_COLOR']))
        embed.add_field(name = "Wager", value = f"{self.wager} Zoid Tokens")
        embed.add_field(name = "Emojis", value = self.emojis)
        embed.set_footer(text = "Match 3 slots to win!")
        view = SlotView(self.interaction, self.wager, self.emojis)
        await view.update_buttons(interaction)
        await interaction.message.edit(embed = embed)
    
    @discord.ui.button(label = "Cancel Bet", custom_id = "cancel_bet", style = discord.ButtonStyle.red, row = 0, disabled = False)
    async def cancel_bet(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user != self.interaction.user:
            return await interaction.response.defer()
        embed = discord.Embed(color=discord.Color.from_str(self.data['EMBED_COLOR']),
                              description=f"You have successfully cancelled this wager.")
        await interaction.message.edit(view=None, embed=embed)
        await interaction.response.defer()


class SlotView(discord.ui.View):
    def __init__(self, interaction, wager, emojis) -> None:
        self.interaction : discord.Interaction = interaction
        self.wager : int = wager 
        self.emojis : int = emojis
        self.emoji_list = ["<:HeartBoost:1209628674823950346>", "<:StarToken:1209628696520958004>", "<:PokerCoin:1209628673142165525>", "<:MagicTrick:1209628688476540979>", "<:boost:1208826731075600426>"]
        self.emojis_using = self.emoji_list[:self.emojis]
        super().__init__(timeout = None)
        self.board = [[random.choice(self.emojis_using) for _ in range(3)] for _ in range(5)]

    async def update_buttons(self, interaction: discord.Interaction):
        for index, child in enumerate(self.children):
            if index != 15:
                child.emoji = self.board[child.row][index % 3]
        await interaction.message.edit(view = self)

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "00", style = discord.ButtonStyle.grey, disabled = True, row = 0)
    async def zero_zero(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "01", style = discord.ButtonStyle.grey, disabled = True, row = 0)
    async def zero_one(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "02", style = discord.ButtonStyle.grey, disabled = True, row = 0)
    async def zero_two(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "10", style = discord.ButtonStyle.grey, disabled = True, row = 1)
    async def one_zero(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "11", style = discord.ButtonStyle.grey, disabled = True, row = 1)
    async def one_one(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "12", style = discord.ButtonStyle.grey, disabled = True, row = 1)
    async def one_two(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(emoji = "<:StarToken:1209628696520958004>", custom_id = "20", style = discord.ButtonStyle.blurple, disabled = True, row = 2)
    async def two_zero(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:StarToken:1209628696520958004>", custom_id = "21", style = discord.ButtonStyle.blurple, disabled = True, row = 2)
    async def two_one(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:StarToken:1209628696520958004>", custom_id = "22", style = discord.ButtonStyle.blurple, disabled = True, row = 2)
    async def two_two(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "30", style = discord.ButtonStyle.grey, disabled = True, row = 3)
    async def three_zero(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "31", style = discord.ButtonStyle.grey, disabled = True, row = 3)
    async def three_one(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "32", style = discord.ButtonStyle.grey, disabled = True, row = 3)
    async def three_two(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "40", style = discord.ButtonStyle.grey, disabled = True, row = 4)
    async def four_zero(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "41", style = discord.ButtonStyle.grey, disabled = True, row = 4)
    async def four_one(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(emoji = "<:TicTacToe:1209654300309979156>", custom_id = "42", style = discord.ButtonStyle.grey, disabled = True, row = 4)
    async def four_two(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(label = "Spin!", custom_id = "spin", style = discord.ButtonStyle.green, disabled = False, row = 4)
    async def spin(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user != self.interaction.user:
            return await interaction.response.defer()
        await interaction.response.defer()
        self.spin.disabled = True
        for _ in range(random.randint(5, 8)):
            self.board.pop()
            self.board.insert(0, [random.choice(self.emojis_using) for _ in range(3)])
            await self.update_buttons(interaction)
            await asyncio.sleep(1)
        if self.two_zero.emoji == self.two_one.emoji == self.two_two.emoji:
            winnings = self.emojis * self.wager
            await interaction.followup.send(content = f"✅ Congratulations you have won `{winnings} Zoid Tokens`!", ephemeral = True)
            lvl_mng = LevelingManager(interaction.user, interaction.channel, winnings)
            await lvl_mng.update()
        else:
            winnings = -self.wager
            await interaction.followup.send(content = "❌ Sorry, but you didn't win!", ephemeral = True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Slots(client))
