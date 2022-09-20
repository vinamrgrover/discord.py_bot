from nextcord.ext import commands
import nextcord, re
import random, os, json, requests
from dotenv import load_dotenv
from nextcord import Embed, ButtonStyle
from nextcord.ui import Button, View

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

try:
    client.remove_command('help')  # to remove the default help command
    help_commands = json.load(open('../help.json'))
except Exception as e:
    print(e)


def createHelpPages(page : int):
    page = page % len(help_commands)  # to avoid out of range
    title = list(help_commands)[page]
    embed = Embed(color = 0xFF512C, title = title)
    for key, val in help_commands[title].items():
        embed.add_field(name = client.command_prefix + key, value = val, inline = False)
        embed.set_footer(text = f'Page {page + 1} of {len(help_commands)}')
    return embed


@client.command(name = 'help')
async def help(ctx):
    current_page = 0

    async def next_callback(interaction):
        nonlocal current_page, sent_message
        current_page += 1
        await sent_message.edit(embed = createHelpPages(current_page), view = help_view)

    async def prev_callback(interaction):
        nonlocal current_page, sent_message
        current_page -= 1
        await sent_message.edit(embed = createHelpPages(current_page), view = help_view)

    next_button = Button(label = '>', style = ButtonStyle.danger)
    next_button.callback = next_callback
    prev_button = Button(label = '<', style = ButtonStyle.danger)
    prev_button.callback = prev_callback

    help_view = View(timeout=100)
    help_view.add_item(prev_button)
    help_view.add_item(next_button)

    sent_message = await ctx.send(embed = createHelpPages(current_page), view = help_view)


# for testing button
@client.command(name = 'temp')
async def temp(ctx):
    embed = Embed(color = 0xFF512C, title = 'Sample')
    button = Button(label = '>', style = ButtonStyle.blurple)
    view = View(timeout = 100)
    view.add_item(button)

    message_sent = await ctx.send(embed = embed, view = view)


@client.command(name = 'dog')
async def dog(ctx):
    url = 'https://dog.ceo/api/breeds/image/random'
    json_response = requests.get(url).json()
    image = json_response['message']
    await ctx.send(image)


@client.command(name = 'cat')
async def cat(ctx):
    load_dotenv(dotenv_path = '../key.env')
    api_key = os.getenv('CAT_API_KEY')
    headers = {'x-api-key' : api_key}
    if api_key is not None:
        url = 'https://api.thecatapi.com/v1/images/search'
        json_response = requests.get(url, headers = headers).json()[0]
        image = json_response['url']
        await ctx.send(image)


@client.command(name = 'cringe')
async def cringe(ctx):

    def get_joke(url, key): # to speed up the response time
        json_response = requests.get(url).json()
        joke_content = json_response[key]
        return joke_content

    url_one = 'https://indian-jokes-api.herokuapp.com/jokes/random'
    url_two = 'https://hindi-jokes-api.onrender.com/jokes'

    embed = Embed(
        color = 0xEDFF17,
        title = "Here's a Cringe WhatsApp joke"
    )

    joke = random.choice([get_joke(url_one, 'text'), get_joke(url_two, 'jokeContent')])

    embed.add_field(name = 'JOKE:', value = joke, inline = False)

    await ctx.send(embed = embed)


@client.command(name = 'insult')
async def insult(ctx, person):
    url = 'https://evilinsult.com/generate_insult.php?lang=en&type=json'
    json_response = requests.get(url).json()
    insult = json_response['insult']
    await ctx.send(person + ', ' + insult)


@client.command(name = 'weather')
async def weather(ctx, location):
    load_dotenv(dotenv_path = '../key.env')
    api_key = os.getenv('WEATHER_API_KEY')
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'

    embed = Embed(
        color = 0x00FFFF,
        title = "Weather for " + location
    )
    error_response = {"error":{"code":1006,"message":"No matching location found."}}

    json_response = requests.get(url).json()

    embed.add_field(
        name = 'Celsius: ',
        value = str(json_response['current']['temp_c']) + ' C',
        inline = False
        )

    embed.add_field(
        name = 'Fahrenheit',
        value = str(json_response['current']['temp_f']) + ' F',
        inline = False
    )

    icon = "https:" + json_response['current']['condition']['icon']

    embed.set_thumbnail(url = icon)

    if json_response != error_response: # for validating location name
        await ctx.send(embed = embed)

    else:
        await ctx.send('Please enter a valid location name!')


@client.event
async def on_ready():
    print(f'{client.user.name} is ready!')


try:
    load_dotenv(dotenv_path = 'path.env')
    PATH = os.getenv('TOKEN_PATH')
    with open(PATH, 'r') as TOKEN:
        client.run(TOKEN.read())
        TOKEN.close()
except Exception as e:
    print(e)
