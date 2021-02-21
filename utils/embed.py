import discord
from typing import Optional, Union
import utils
import config

color = config.embed_color

def info_embed(title: str = None, description: str = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    return embed

def error_embed(title: str = None, description: str = None, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed

def normal_embed(title: str = None, description: str = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if author:
        embed.set_footer(text=author, icon_url=str(author.avatar_url))
    return embed