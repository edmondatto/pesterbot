import os
import slackclient
import time
import random

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SOCKET_DELAY = 1

# Pester bot env variables
PESTER_SLACK_NAME = os.environ.get('PESTER_SLACK_NAME')
PESTER_SLACK_TOKEN = os.environ.get('PESTER_SLACK_TOKEN')
PESTER_SLACK_ID = os.environ.get('PESTER_SLACK_ID')

pester_slack_client = slackclient.SlackClient(PESTER_SLACK_TOKEN)


def get_mention(user):
    return '<@{user}>'.format(user=user)


pester_slack_mention = get_mention(PESTER_SLACK_ID)


def is_private(event):
    return event.get('channel').startswith('D')


def is_for_me(event):
    """Know if the message is dedicated to me"""
    # check if not my own event
    event_type = event.get('type')
    if event_type and event_type == 'message' and not (event.get('user') == PESTER_SLACK_ID):
        # in case it is a private message return true
        if is_private(event):
            return True
        # in case it is not a private message check mention
        text = event.get('text')
        channel = event.get('channel')
        if pester_slack_mention in text.strip().split():
            return True


def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['hello', 'mambo', 'hey', 'hi', 'sup', 'morning', 'hola', 'sema', 'habari'])


def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens for g in ['bye', 'goodbye', 'revoir', 'adios', 'later', 'cya'])


def say_hi(user_mention):
    """Say Hi to a user by formatting their mention"""
    response_template = random.choice(['Sup, {mention}...',
                                       'Yo!',
                                       'Hola {mention}',
                                       'Bonjour!'])
    return response_template.format(mention=user_mention)


def say_bye(user_mention):
    """Say Goodbye to a user"""
    response_template = random.choice(['see you later, alligator...',
                                       'adios amigo',
                                       'Bye {mention}!',
                                       'Au revoir!'])
    return response_template.format(mention=user_mention)


def handle_message(message, user, channel):
    if is_hi(message):
        user_mention = get_mention(user)
        post_message(message=say_hi(user_mention), channel=channel)
    elif is_bye(message):
        user_mention = get_mention(user)
        post_message(message=say_bye(user_mention), channel=channel)


def post_message(message, channel):
    pester_slack_client.api_call('chat.postMessage', channel=channel, text=message, as_user=True)


def run():
    if pester_slack_client.rtm_connect():
        print('[.] Pester is ON...')
        while True:
            event_list = pester_slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if is_for_me(event):
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')


if __name__ == '__main__':
    run()
