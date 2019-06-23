import os
import json
import distutils.util
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Slack
SLACK_HOOK_URL = os.environ['SLACK_HOOK_URL']

# dryrun
dry_run = bool(distutils.util.strtobool(os.getenv("dry_run", "False")))


def send_to_slack(**attachments):
    payload = {"attachments": [attachments]}
    data = "payload=" + json.dumps(payload)
    if not dry_run:
        req = Request(SLACK_HOOK_URL, data=data.encode("utf-8"), method="POST")
        try:
            response = urlopen(req)
            response.read()
            print("Message posted to %s", SLACK_HOOK_URL)
        except HTTPError as e:
            print("Request failed: %d %s", e.code, e.reason)
        except URLError as e:
            print("Server connection failed: %s", e.reason)
