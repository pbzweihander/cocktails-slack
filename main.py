
from slackclient import SlackClient
from cocktaildb import *
import time

BOT_NAME = "bartender-bot"
BOT_ID = ''

slack_client = SlackClient(open('token.key', 'r').readline().strip())


def parse_slack_output(output):
    if output and len(output) > 0:
        print(output)
        for o in output:
            if o and 'text' in o and o.get('user') != BOT_ID:
                return o.get('text').strip(), o.get('channel')
    return None, None


def handle_command(command: str, channel: str):
    if command.startswith('c?'):
        name = command.split('c?')[1].strip()
        if name == 'random':
            s = random_cocktails()
        else:
            s = find_cocktails(name)
        if s:
            slack_client.api_call('chat.postMessage', channel=channel, text=s, as_user=True)
        else:
            slack_client.api_call('chat.postMessage', channel=channel, text='._.', as_user=True)
    if command.startswith('i?'):
        name = command.split('i?')[1].strip()
        s = find_ingredient(name)
        if s:
            slack_client.api_call('chat.postMessage', channel=channel, text=s, as_user=True)
        else:
            slack_client.api_call('chat.postMessage', channel=channel, text='._.', as_user=True)


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
