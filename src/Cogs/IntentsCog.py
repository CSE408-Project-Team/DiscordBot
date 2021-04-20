

from discord.ext import commands
import Lib.Intent as Intent


def setup(bot):
    bot.add_cog(IntentsCog(bot))

class IntentsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def learn(self, ctx):
        await ctx.send("**Learning...**")

    @commands.command()
    async def getIntent(self, ctx, *text):
        text = " ".join(text)
        await ctx.send(Intent.classifyText(text)[0])

    @commands.command()
    async def getConfidence(self, ctx, *text):
        text = " ".join(text)
        response, confidence = Intent.getResponse(text)
        await ctx.send("Confidence: " + str(confidence))

    @commands.command()
    async def talk(self, ctx, *text):
        text = " ".join(text)
        print(text)
        response, confidence = Intent.getResponse(text)

        if confidence > .7:
            await ctx.send(Intent.getResponse(text)[0]) 
        else:
            await ctx.send("I'm not sure I understand")

