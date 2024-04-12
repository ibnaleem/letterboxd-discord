import letterboxdpy
import discord, os, requests
from discord import app_commands
from discord import Embed, Intents, Interaction

LETTERBOXD_DISCORD_TOKEN = os.getenv("LETTERBOXD_DISCORD_TOKEN")

client = discord.Client(intents=Intents.all())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready() -> None:
    try:
        await tree.sync()
        await client.change_presence(activity=discord.Streaming(name="/help", url="https://twitch.tv/gothamchess"))
        print(f"----- {client.user.name} is Online -----\nServers: {len(client.guilds)}\nMembers: {len(client.users)}")

    except Exception:
        print(Exception)

client.run(LETTERBOXD_DISCORD_TOKEN)
