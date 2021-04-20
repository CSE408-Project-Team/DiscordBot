
from discord.ext import commands
import Lib.sentimentAnalysis as SA


def setup(bot):
    bot.add_cog(SentimentCog(bot))


class SentimentCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.users = []

    @bot.event()
    async def on_message(message):
        print("ah")


    @commands.command()
    async def getSentiment(self, ctx, *text):
        text = " ".join(text)
        await ctx.send(SA.sumScores(text))

