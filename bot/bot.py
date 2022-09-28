from nextcord.ext import commands
import nextcord, re, discord
import random, os, json, requests
from dotenv import load_dotenv
from nextcord import Embed, ButtonStyle
from nextcord.ui import Button, View
import sqlite3 as sql
import datetime


try:

    intents = nextcord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True

    client = commands.Bot(command_prefix = '!', intents = intents)

except Exception as e:
    print(e)


@client.command(name = 'hey')
async def hey(ctx):
    await ctx.send(f'Hey {ctx.author.mention}!')


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
    embed = Embed(color = discord.Color.blurple(), title = title)
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

    next_button = Button(label = '>', style = ButtonStyle.blurple)
    next_button.callback = next_callback
    prev_button = Button(label = '<', style = ButtonStyle.blurple)
    prev_button.callback = prev_callback

    help_view = View(timeout=100)
    help_view.add_item(prev_button)
    help_view.add_item(next_button)

    sent_message = await ctx.send(embed = createHelpPages(current_page), view = help_view)


# for testing button
@client.command(name = 'temp')
async def temp(ctx):
    print(ctx.author.mention)
    print(ctx.author.avatar)

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
    insult_content = json_response['insult']
    person = person + ', '
    await ctx.send(f'{person}{insult_content}')


@client.command(name = 'weather')
async def weather(ctx, location):
    load_dotenv(dotenv_path = '../key.env')
    api_key = os.getenv('WEATHER_API_KEY')
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'

    embed = Embed(
        color = 0x00FFFF,
        title = "Weather for " + location
    )

    json_response = requests.get(url).json()

    error_response = {"error": {"code": 1006, "message": "No matching location found."}}

    if json_response == error_response:
        await ctx.send('Please enter a valid location name!')

    variables = {
        "temp_c" : str(json_response['current']['temp_c']) + ' C',
        "temp_f" : str(json_response['current']['temp_f']) + ' F',
        "Condition" : str(json_response['current']['condition']['text']),
        "icon" : "https:" + json_response['current']['condition']['icon'],
    }

    embed.add_field(
        name = 'Celsius: ',
        value = variables['temp_c'],
        inline = False
        )

    embed.add_field(
        name = 'Fahrenheit: ',
        value = variables['temp_f'],
        inline = False
    )

    embed.add_field(
        name = 'Condition: ',
        value = variables['Condition'],
        inline = False
    )

    embed.set_thumbnail(url = variables['icon'])

    await ctx.send(embed = embed)


@client.command(name = 'gay')
async def gay(ctx, *args : discord.Mentionable):
    images = {
        'pic_1' : 'https://c.tenor.com/MDByA_41JrUAAAAC/chakke-gay.gif',
        'pic_2' : 'https://i.pinimg.com/originals/73/b5/e7/73b5e75f41944cf3794995cd343d565f.gif',
        'pic_3' : 'https://c.tenor.com/QDi3u5djy_8AAAAC/gay-ha.gif'
    }

    json_file = json.load(open('../responses.json'))
    responses_args = json_file['Gay']['list']
    responses = json_file['Gay']['list_personal']

    percentage  = random.randrange(101)

    if len(args) == 0:
        embed = Embed(
            color = discord.Color.random(),
            description = random.choice(responses).format(percentage)
        )
    else:
        args = args[0]
        embed = Embed(
            color = discord.Color.random(),
            description = random.choice(responses_args).format(args, percentage)
        )

    if percentage > 80:
        url = images['pic_1']
    elif percentage > 50:
        url = images['pic_2']
    else:
        url = images['pic_3']

    embed.set_image(url = url)

    await ctx.send(embed = embed)


client.command(name = 'cool')
async def cool(ctx):

    json_file = json.load(open('../responses.json'))
    responses = json_file['Cool']['list_personal']

    percentage = random.randrange(101)

    embed = Embed(
        color = discord.Color.random(),
        description = random.choice(responses).format(percentage)
    )

    await ctx.send(embed = embed)


@client.command(name = 'dadjoke')
async def dadjoke(ctx):

    url = 'https://icanhazdadjoke.com/'
    json_response = requests.get(url, headers={"Accept": "application/json"}).json()

    joke =  '**' + json_response['joke'] + '**'

    embed = Embed(
        color=discord.Color.random(),
        description = joke
    )

    await ctx.send(embed = embed)


@client.slash_command(name = 'fortune', description = 'Know your luck')
async def fortune(ctx : nextcord.Interaction, question : str):
    json_file = json.load(open('../responses.json'))
    responses = json_file['fortune']['list']
    await ctx.response.send_message(f'**User: **{question}\n**Response: **{random.choice(responses)}')


def verify_profile(user_id) -> bool:
    try:
        conn = sql.connect('../db/database.db')
        cur = conn.cursor()
        query = f"""
        SELECT * FROM USER_INFO
        WHERE ID = "{user_id}";
        """

    except sql.Error as e:
        print(e)

    cur.execute(query)

    if cur.fetchall() == list():  # if the result is an empty list
        return False
    else:
        return True


@client.slash_command(name = 'whois', description = 'Get user\'s info(use /profile to create your\'s')
async def whois(ctx : discord.Interaction, user_id : discord.Member):

    def get_status(member : discord.Member):
        if str(member.status) ==  'online':
            return True

        return False

    get_status(user_id)

    try:
        conn = sql.connect("../db/database.db")
        cur = conn.cursor()

        discord_tag = user_id.name + '#' + user_id.discriminator
        print(discord_tag)


        query = f"""
        SELECT * FROM USER_INFO 
        WHERE ID = {user_id.id}
        """

        print(query)

        cur.execute(query)

        try:
            res = cur.fetchall()[0]
        except:
            res = tuple()

        if len(res) == 0:
            await ctx.send("***No records found!***")

        else:
            name = str(user_id.name) + '\'s '

            embed = Embed(title = f'{name} Profile'.capitalize(), color = discord.Color.green())

            embed.add_field(name = '**Name: **', value = res[1])

            embed.add_field(name = '**About: **', value = res[2])

            embed.add_field(name = '**Fav Emoji: **', value = res[3], inline = False)

            embed.set_footer(text = f'DATE CREATED: {res[4]}')

            embed.add_field(name = '**Account created on: **', value = user_id.created_at.date())

            embed.set_author(name = 'Otter Profile', icon_url = user_id.avatar)

            embed.add_field(name = 'Status', value = '*Online*' if get_status(user_id) else '*Offline*')

            avatar = user_id.avatar

            if avatar is None:
                avatar = user_id.default_avatar

            embed.set_thumbnail(url = avatar)

            await ctx.send(embed = embed)

        print(res, type(res))

    except sql.Error as e:
        print(e)


@client.slash_command(name = 'profile', description = 'create your own "whois" profile')
async def profile(ctx, name : str, about_you : str, emoji):
    try:
        conn = sql.connect("../db/database.db")
        cur = conn.cursor()

        query = """
        INSERT INTO USER_INFO VALUES
        (?, ?, ?, ?, ?)
        """

        user_id = ctx.user.id

        if verify_profile(user_id):
            await ctx.send("**Profile already exists**")

        else:
            cur.execute(query, (user_id, name, about_you, emoji, datetime.date.today()))

            conn.commit() # committing the changes

            cur.execute("SELECT * FROM USER_INFO")

            print(cur.fetchall())

            conn.close()

            await ctx.send(f'Profile for user {ctx.user.mention} successfully created!')

    except sql.Error as e:
        await ctx.send('OOPS Something wrong happened please try again')
        print(e)


@client.command(name = 'test')
async def test_mention(ctx, user_id : discord.Member):
    print(user_id.id)
    print(user_id.status)

    print(ctx.author.id)
    discord_tag = user_id.name + '#' + user_id.discriminator
    if verify_profile(discord_tag) is True:
        await ctx.send("SUCCESS")
    else:
        await ctx.send("FAILED")


@client.event
async def on_ready():
    try:
        conn = sql.connect('../db/database.db')
        cur = conn.cursor()

        cur.execute("""
        DROP TABLE IF EXISTS USER_INFO;
        """)

        conn.commit()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS USER_INFO
        (            
            ID BIGINT PRIMARY KEY, 
            NAME VARCHAR(20), 
            DESCRIPTION VARCHAR(100), 
            FAV_EMOJI VARCHAR(30), 
            DATE_CREATED DATE
        ); 
        """)

    except sql.Error as e:
        print(e)

    print(f'{client.user.name} is ready!')


try:
    load_dotenv(dotenv_path = 'path.env')
    PATH = os.getenv('TOKEN_PATH')
    with open(PATH, 'r') as TOKEN:
        client.run(TOKEN.read())
        TOKEN.close()
except Exception as e:
    print(e)

