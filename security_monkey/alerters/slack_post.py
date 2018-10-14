# Houses functions used to compose slack messages to send to Slack
#
# Changes in here will directly affect what messages you receive in slack
# Written by :: Ankur Shah <ankurpshah@gmail.com>
# Date :: October 2018
#

import slackweb
import os
import json
import requests


def postMessage(attachments):

    slack = slackweb.Slack(url="https://hooks.slack.com/services/XXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXXXX")


    slack.notify(
        channel="#security-compliance",
        attachments = attachments,
        username='SecurityMonkey Bot',
        icon_emoji=":monkey:",
        footer="Security Monkey Team"
        )
