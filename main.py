import discord
import platform
from discord.ext import commands, tasks
import os
from Tools.utils import getConfig, getGuildPrefix, updateConfig
from asyncio import sleep
import asyncio
import json
from dislash import InteractionClient, ActionRow, Button, ButtonStyle
from reactionmenu import ReactionMenu, Button, ButtonType
from discord import Client, Intents, Embed
import time
from discord import Intents, Activity
from collections import defaultdict
import threading
from discord_slash.utils.manage_commands import create_option, create_choice
from collections import defaultdict
import shutil
from shutil import rmtree
import datetime
from reactionmenu import ButtonsMenu, ComponentsButton
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(getGuildPrefix, help_command=None, intents=intents)
ButtonsMenu.initialize(client)
client.sniped_messages = {}
client.warnings = {}
starttime = datetime.datetime.utcnow()


@client.command()
async def load(extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def reload(extension):
    client.reload_extension(f'cogs.{extension}')


@client.command()
async def unload(extension):
    client.unload_extension(f'cogs.{extension}')

# Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    pythonVersion = platform.python_version()
    print(f'We have logged in as {client.user}')
    print(discord.__version__)
    print(pythonVersion)


@client.event
async def on_guild_join(guild):
    data = getConfig(guild.id)
    data["owner"] = guild.owner_id
    updateConfig(guild.id, data)

    bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
    try:
        join = discord.Embed(title="Thanks for adding Server Security", colour=discord.Colour.blue(),
                             description=f"**Some Information**\n"
                                         f"With some powerful features, Server Security will be able to protect your server from being nuked, raiders, malicous users, spammer etc. and still it gives you additional features, such as some moderation commands and all of these are free. Make sure Server Security has the highest possible role on your server, also the bot won't function without having the Administrator permission.")
        await bot_entry[0].user.send(embed=join)
    except discord.errors.Forbidden:
        pass




@client.event
async def on_guild_remove(guild):
    with open("config.json", "r") as f:
        data = json.load(f)

    del data["guilds"][str(guild.id)]

    with open("config.json", "w") as f:
        json.dump(data, f)


#@tasks.loop(seconds=10)
#async def statusloop():
#    await client.wait_until_ready()
#    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"s!help"))
#    await sleep(10)
#    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(client.guilds)} guilds"))
#    await sleep(10)
#    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(set(client.get_all_members()))} members"))
#    await sleep(10)
#statusloop.start()


@client.event
async def on_message_delete(message):
    try:
        client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)
    except AttributeError:
        pass


@client.command(name="snipe",
                description="Snipes the last deleted message")
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Colour.blue(), timestamp=time,
                          title="Sniped Message")
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text="Deleted in: #{0}".format(channel_name))

    await ctx.channel.send(embed=embed)


@client.command(name="uptime",
                description="Shows you Server Security's Uptime")
async def uptime(ctx):
    uptime = datetime.datetime.utcnow() - starttime
    uptime = str(uptime).split('.')[0]
    embed = discord.Embed(title="Server Security's Uptime", description=f"```{uptime}```",
                          color=discord.Colour.blue())
    await ctx.send(embed=embed)


client.run("OTMzOTYwNDIyODEyNDIyMTU0.YepIbA.rUkc6uAMXVzwnWwC5xdGNA9On_w")
