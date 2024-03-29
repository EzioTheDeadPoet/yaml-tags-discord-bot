import os

import discord
import requests
import yaml
from dotenv import load_dotenv

load_dotenv()

tag_index = os.getenv('TAG_INDEX')


async def tags(ctx: discord.AutocompleteContext):
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
    tag_content = ""
    if response.status_code == 200:
        response_data = yaml.safe_load(response.text)
        tag_response = requests.get(response_data[tag], stream=True)
        if tag_response.status_code == 200:
            tag_content = tag_response.text
    return tag_content
