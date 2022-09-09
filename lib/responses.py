import random


def handle_response(message : str, author : str) -> str:
    mod_message = message.lower()

    if mod_message == 'hello':
        return 'Hello' + author

    if mod_message == 'toss':
        return str(random.choice(['Its Heads!',
                                  'Its Tales!']))

    if mod_message == 'help':
        return '''`Help Section \n
        Commands List: hello \n toss`'''