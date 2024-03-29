import os
import discord
from dotenv import load_dotenv
from rest_repository import get

load_dotenv()

token = os.getenv("DISCORD_BOT_TOKEN")
bot = discord.Bot()


@bot.slash_command(name="tags", description="Get tag responses")
async def wiki_search(
        ctx: discord.ApplicationContext,
        tag: discord.Option(str, choices=get.tags())):
    embed = discord.Embed(
        description=get.content(tag),
        color=discord.Color.from_rgb(216, 186, 248))
    embed.set_author(name=f"Tag:{tag}")
    await ctx.respond(embed=embed)


bot.run(token)
