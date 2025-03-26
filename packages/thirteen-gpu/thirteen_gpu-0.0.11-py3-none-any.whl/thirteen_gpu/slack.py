import os
from slack_sdk import WebClient


def slack_alarm(message: str, stdout: bool = False, tag_user: str = None):
    channel_id = os.getenv("SLACK_NOTIFICATION_CHANNEL", "#general")
    token = "xoxb-3302781179860-3669961381395-RWbYFzXaqf8TpczM6KkE8575"

    client = WebClient(token)
    user_info = {
        "seilna": "U038UCRMDMH",
        "forybm": "U03FJ62V8CF",
        "joohong": "U03FYS88ZUH",
        "lynch": "U03FJ62V8CF",
    }
    
    if tag_user:
        message = f"<@{user_info[tag_user]}> {message}"

    client.chat_postMessage(channel=channel_id, text=message)
