import os

import discord
import requests
import yaml
from dotenv import load_dotenv

load_dotenv()

tag_index = os.getenv('TAG_INDEX')


async def tags(ctx: discord.AutocompleteContext):
    await ctx.interaction.response.defer()
    response = requests.get(tag_index, stream=True)
    tags_list = []
    if response.status_code == 200:
        response_data = yaml.safe_load(response.text)
        for tag in response_data:
            tags_list.append(tag)
    return sorted([i for i in tags_list
                   if (i.startswith(ctx.value.lower())
                       or i.startswith(ctx.value.upper()))])


def content(tag: str):
    response = requests.get(tag_index, stream=True)
    tag_content = {"text": "", "image_url": ""}
    if response.status_code == 200:
        response_data = yaml.safe_load(response.text)
        tag_response = requests.get(response_data[tag]["text"], stream=True)
        if tag_response.status_code == 200:
            tag_content["text"] = tag_response.text
        if tag_response.status_code == 404:
            tag_content["text"] = ("404: Tag content not found.\n"
                                   f"This implies a broken source URL in the [tag index]({tag_index}).")
        try:
            tag_content["image_url"] = response_data[tag]["image_url"]
        except KeyError:
            tag_content["image_url"] = ""
    return tag_content
