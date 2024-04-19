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
        tag: discord.Option(str, description="choose a tag", autocomplete=get.tags)):
    content = {"text": "Tag not found", "image_url": ""}
    ephemeral = False
    truncated_amount = 0
    try:
        content = get.content(tag)
    except KeyError:
        ephemeral = True
    content_text = content["text"]
    content_image_url = content["image_url"]
    if len(content_text) > 4096:
        truncated_amount = len(content_text) - 4096
        content_text = content_text[:4096]

    embed = discord.Embed(
        description=content_text,
        color=discord.Color.from_rgb(216, 186, 248))
    embed.set_author(name=f"Tag:{tag}")
    if len(content_image_url) > 0:
        embed.set_image(url=content_image_url)
    await ctx.respond(embed=embed, ephemeral=ephemeral)
    if truncated_amount > 0:
        await ctx.respond(f"*The content of `{tag}` has been truncated by `{truncated_amount}` characters "
                          f"to fit the `4096` character limit.\n"
                          f"Please shorten the tag content to fix this.*")


bot.run(token)
