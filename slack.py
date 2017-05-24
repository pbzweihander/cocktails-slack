
from slackclient import SlackClient


class Slack:
    client = None
    name = ""
    id = ""
    connected = False

    def __init__(self, token: str, name: str):
        self.client = SlackClient(token)
        self.name = name

        api_call = self.client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.name:
                    self.id = user.get('id')
                    break

    def connect(self) -> bool:
        self.connected = self.client.rtm_connect()
        return self.connected

    @staticmethod
    def parse_slack_output(output: list) -> dict:
        if output and len(output) > 0:
            for o in output:
                if o and 'text' in o:
                    return o
        return {}

    def post_message(self, chan: str, msg: str):
        if self.connected:
            self.client.api_call('chat.postMessage', channel=chan, text=msg, as_user=True)

    def read(self) -> dict:
        if self.connected:
            return self.parse_slack_output(self.client.rtm_read())
