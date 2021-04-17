
import discord
from discord.ext import commands


Bot = commands.Bot(command_prefix=',,')

@Bot.event
async def on_ready():
    print(f"Logged in as {Bot.user}")
