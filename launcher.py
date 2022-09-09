from dotenv import load_dotenv
import os
import bot.bot as _BotClass

if __name__ == '__main__':
    load_dotenv(dotenv_path = 'token.env')

    TOKEN = os.getenv('DISCORD_TOKEN')

    Bot = _BotClass.Bot()

    try:
        Bot.client.run(TOKEN)
    except Exception as e:
        print(e)

