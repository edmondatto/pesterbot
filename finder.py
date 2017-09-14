import os
import slackclient

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PESTER_SLACK_NAME = os.environ.get('PESTER_SLACK_NAME')
PESTER_SLACK_TOKEN = os.environ.get('PESTER_SLACK_TOKEN')

# Fire up slack client
pester_slack_client = slackclient.SlackClient(PESTER_SLACK_TOKEN)

# check if everything is alright and retrieving bot ID
is_valid = pester_slack_client.api_call("users.list").get('ok')
if is_valid:
    for user in pester_slack_client.api_call("users.list").get('members'):
        if user.get('name') == PESTER_SLACK_NAME:
            print(user.get('id'))
