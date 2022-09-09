from lib import responses


async def send_message(message, user_message, private : bool):

    response = responses.handle_response(user_message, ' ' + str(message.author.name))

    try:
        if private:
            await message.author.send(response)
        else:
            await message.channel.send(response)

    except Exception as e:
        print(e)

