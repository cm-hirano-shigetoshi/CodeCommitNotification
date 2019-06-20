from slackclient import SlackClient
import os
import distutils.util

# Slack
slack_client = None
slack_token = os.environ["SLACK_TOKEN"]
slack_channel = os.getenv('SLACK_CHANNEL', "#build_information")

# dryrun
dry_run = bool(distutils.util.strtobool(os.getenv("dry_run", "False")))


def send_to_slack(event):
    global slack_client
    global dry_run
    if not slack_client:
        slack_client = SlackClient(slack_token)
    if "message" in event:
        message = event['message']
    else:
        message = None
    if "attachments" in event:
        attachments = event['attachments']
    else:
        attachment = None
    if not dry_run:
        if message or attachment:
            slack_client.api_call(
                "chat.postMessage",
                channel=slack_channel,
                attachments=attachments,
                text=message)

