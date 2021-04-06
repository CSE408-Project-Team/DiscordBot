
import os
import json
from pathlib import Path

import discord
from Bot import Bot


with open('./config.json') as f:
    data = json.load(f)

token = data["Token"]


"""
Add functionality by creating files in ./Cogs and following the format in Testing.py.
After the cog is made for the first time, you can hot-reload your edits by using the m!reload command.
It will not work for the first time the file is made however, you will have to manually stop the bot.

Make sure to include:
def setup(bot):
    bot.add_cog(COG_NAME(bot))
"""

cwd = str(Path(__file__).parents[0])


if __name__ == "__main__":

    for file in os.listdir(cwd+"/Cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            Bot.load_extension(f"Cogs.{file[:-3]}")

    # TODO hide the token in a JSON or env file later 
    Bot.run(token)