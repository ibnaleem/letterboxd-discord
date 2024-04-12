from letterboxdpy import user
from discord import app_commands
import discord, os, requests, random, json
from discord import Embed, Intents, Interaction

LETTERBOXD_DISCORD_TOKEN = os.getenv("LETTERBOXD_DISCORD_TOKEN")
COLOURS = [0xff8000, 0x00e054, 0x40bcf4]

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

@tree.command(description="Fetch Letterboxd Profile")
@app_commands.describe(username="Found after the / in letterboxd.com")
async def profile(interaction: Interaction, username: str):
    profile_data = user.User(username)
    json_dict = profile_data.jsonify()

    if json_dict.get("avatar", {}).get("exists"):
        url = json_dict.get("avatar", {}).get("url")
    else:
        url = "https://w7.pngwing.com/pngs/183/847/png-transparent-letterboxd-iphone-app-store-film-iphone-electronics-orange-sphere.png"

    embed = Embed(description=f"[{username}'s Letterboxd Profile](https://letterboxd.com/{username})", color=random.choice(COLOURS))
    embed.set_thumbnail(url=url)
    embed.set_author(name=username, icon_url=url)
    embed.add_field(name="Display name", value=json_dict.get("display_name", ""), inline=True)
    embed.add_field(name="ID", value=json_dict.get("id"), inline=True)
    embed.add_field(name="Bio", value=json_dict.get("bio", ""), inline=True)
    embed.add_field(name="Location", value=json_dict.get("location", ""), inline=True)
    embed.add_field(name="Watchlist length", value=json_dict.get("watchlist_length"), inline=True)
    embed.add_field(name="Films", value=json_dict.get("stats", {}).get("films"), inline=True)  # Using square brackets for nested access
    embed.add_field(name="Films this year", value=json_dict.get("stats", {}).get("this_year"), inline=True)
    embed.add_field(name="Lists", value=json_dict.get("stats", {}).get("list"), inline=True)
    embed.add_field(name="Followers", value=json_dict.get("stats", {}).get("followers"), inline=True)
    embed.add_field(name="Following", value=json_dict.get("stats", {}).get("following"), inline=True)

    await interaction.response.send_message(embed=embed)

client.run(LETTERBOXD_DISCORD_TOKEN)
