import discord
from lib.messages import send_message


class Bot:

    def __init__(self):
        self.client = discord.Client(intents = discord.Intents.all())

        @self.client.event
        async def on_connect():
            print(f'{self.client.user.name} has connected!')

        @self.client.event
        async def on_ready():
            print(f'{self.client.user.name} is ready!')

        @self.client.event
        async def on_message(message):

            if message.author == self.client.user:  # to avoid loop
                return

            user_message = message.content
            author = message.author
            channel = message.channel

            print(f'user {author} has said {user_message} on {channel}')  # for self reference

            if user_message[0] == '!':
                pass

            elif user_message[0] == '.':
                await send_message(message, user_message, True)

            else:
                await send_message(message, user_message, False)



