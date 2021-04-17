

import os
import discord
from discord.ext import commands


"""
Testing and development related commands.

Note: reloading changes here can be volatile, as any errors
will disable the use of the reload command any further for that 
session.
"""

class Testing(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        """Simple ping response"""
        await ctx.send(f"**Pong! In {round(self.bot.latency, 4)}**")


    @commands.command(name='reload', hidden=True)
    async def reload(self, ctx):
        """Hot reload all cogs"""

        embed = discord.Embed(
            title="Reloading cogs",
            color=0x808080,
            timestamp=ctx.message.created_at
        )

        for ext in os.listdir("./src/Cogs/"):
            if ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.bot.unload_extension(f"Cogs.{ext[:-3]}")
                    self.bot.load_extension(f"Cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Reloaded: `{ext}`",
                        value='\uFEFF',
                        inline=True
                    )
                except Exception as e:
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value=e,
                        inline=True
                    )
        await ctx.send(embed=embed)


    @commands.command(
        name='args', 
        hidden=True, 
        description="Show the number of arguments and the arguments themselves")
    async def args(self, ctx, *args):
        await ctx.send(f"**Count = {len(args)}.** \n" + " ".join(args))
        print(args)

    @commands.command()
    async def quit(self, ctx):
        await ctx.send(f"**Quitting...**")
        quit()



def setup(bot):
    bot.add_cog(Testing(bot))