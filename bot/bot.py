from nextcord.ext import commands
import nextcord
import random
import os
from dotenv import load_dotenv

try:

    intents = nextcord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix = '!', intents = intents)

except Exception as e:
    print(e)


@client.command(name = 'hey')
async def hey(ctx):
    await ctx.send(f'Hey {ctx.author.name}!')


@client.command(name = 'toss', aliases = ['TOSS', 'Toss'])
async def toss(ctx):
    res = random.choice(['Its Heads!', 'Its Tales!'])
    await ctx.send(res)


@client.command(name = 'ping')
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000, 2)} ms!')


@client.event
async def on_ready():
    print(f'{client.user.name} is ready!')


try:
    load_dotenv(dotenv_path = '../path.env')
    PATH = os.getenv('TOKEN_PATH')
    with open(PATH, 'r') as TOKEN:
        client.run(TOKEN.read())
        TOKEN.close()
except Exception as e:
    print(e)

