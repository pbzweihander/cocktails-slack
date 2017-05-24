
from slack import Slack
from cocktaildb import *
import time

BOT_NAME = "bartender-bot"

slack = Slack(open('token.key', 'r').readline().strip(), BOT_NAME)


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
        slack.post_message(channel, s)


def main():
    if slack.connect():
        print("Bot Connected")
        while True:
            d = slack.read()
            if d and d.get('id') != slack.id:
                chan = d.get('channel')
                msg = d.get('text')
                print("Received at %s : %s" % (chan, msg))
                handle_command(msg, chan)
                time.sleep(1)
    else:
        print("Connection Failed")


if __name__ == '__main__':
    main()
