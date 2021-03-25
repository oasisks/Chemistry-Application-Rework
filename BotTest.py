import os
import discord

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")


@client.event
async def on_member_join(member):
    print(f"{member.name} has joined")
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return



client.run(TOKEN)
