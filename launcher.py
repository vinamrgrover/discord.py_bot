import bot.bot as BotClass

if __name__ == '__main__':
    try:
        Bot = BotClass.Bot()

        with open('token.txt', 'r') as TOKEN:
            Bot.client.run(TOKEN.read())

    except Exception as e:
        print(e)

