
from slackclient import SlackClient
from cocktaildb import *
import time

BOT_NAME = "bartender-bot"
BOT_ID = ''

slack_client = SlackClient(open('token.key', 'r').readline().strip())


def parse_slack_output(output):
    if output and len(output) > 0:
        for o in output:
            if o and 'text' in o and o.get('user') != BOT_ID:
                return o.get('text').strip(), o.get('channel')
    return None, None


def post_message(chan, msg):
    print("Post : %s" % msg)
    slack_client.api_call('chat.postMessage', channel=chan, text=msg, as_user=True)


def handle_command(command: str, channel: str):
    s = ''
    if command.startswith('c?'):
        name = command.split('?')[1].strip()
        if name:
            if name == 'random':
                s = random_cocktails()
            else:
                s = find_cocktails(name)
            if not s:
                s = '._.'
    elif command.startswith('cs?'):
        name = command.split('?')[1].strip()
        if name:
            s = find_cocktails(name, True, False)
            if not s:
                s = '._.'
    elif command.startswith('cd?'):
        name = command.split('?')[1].strip()
        if name:
            s = find_cocktails(name, False, True)
            if not s:
                s = '._.'
    elif command.startswith('i?'):
        name = command.split('?')[1].strip()
        if name:
            s = find_ingredient(name)
            if not s:
                s = '._.'
    elif command.startswith('is?'):
        name = command.split('?')[1].strip()
        if name:
            s = find_ingredient(name, True, False)
            if not s:
                s = '._.'
    elif command.startswith('id?'):
        name = command.split('?')[1].strip()
        if name:
            s = find_ingredient(name, False, True)
            if not s:
                s = '._.'
    if s:
        post_message(channel, s)


def main():
    global BOT_ID
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                BOT_ID = user.get('id')
                break
    print('Bot ID Retrieved')

    if slack_client.rtm_connect():
        print("Bot connected")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                print("Received at %s : %s" % (channel, command))
                handle_command(command, channel)
                time.sleep(1)
    else:
        print("Connection Failed")


if __name__ == '__main__':
    main()
