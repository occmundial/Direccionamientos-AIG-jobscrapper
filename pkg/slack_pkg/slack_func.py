from internal.config import configuration as c
from slacker import Slacker


def post_message(message):
    if c.env == 'PROD':
        client = Slacker(token=c.slack_token)
        client.chat.post_message(channel=c.channel, text=message)