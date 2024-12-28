import os
from idlelib.window import add_windows_to_menu

import discord
from dotenv import load_dotenv
from rest_repository import get

print(f"Initializing")

load_dotenv()
try:
    load_dotenv("secrets.env")
except Exception as e:
    print(e)

token = os.getenv("DISCORD_BOT_TOKEN")
bot = discord.Bot()

@bot.slash_command(name="tags", description="Get tag responses")
async def wiki_search(
        ctx: discord.ApplicationContext,
        tag: discord.Option(str, description="choose a tag", autocomplete=get.tags),
        ping: discord.Option(discord.Member, "user to ping", required=False)):
    await ctx.defer()
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
    if ping:
        await ctx.respond(f"{ping.mention} Please read this fully, as it will have the answers you need.",embed=embed, ephemeral=ephemeral)
    else:
        await ctx.respond(embed=embed, ephemeral=ephemeral)
    if truncated_amount > 0:
        await ctx.respond(f"*The content of `{tag}` has been truncated by `{truncated_amount}` characters "
                          f"to fit the `4096` character limit.\n"
                          f"Please shorten the tag content to fix this.*")


print(f"Start Bot")
bot.run(token)