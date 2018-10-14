#     Copyright 2016 Bridgewater Associates
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
"""
.. module: security_monkey.alerters.custom_alerter
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Ankur Shah <ankurpshah@gmail.com>


"""
from security_monkey import app
from slack_post import postMessage
import os

alerter_registry = []
server_url = 'https://security-monkey.myserver.com'


class SlackAlerter(type):

    def __init__(cls, name, bases, attrs):
        if getattr(cls, "report_auditor_changes", None) and getattr(cls, "report_watcher_changes", None):
            app.logger.debug("Registering alerter %s", cls.__name__)
            alerter_registry.append(cls)


def report_auditor_changes(auditor):
    for item in auditor.items:
        for issue in item.confirmed_new_issues:
            # Create a text output of your auditor new issue in scope
            attachments = [{"author_name": "Auditor - Reporting on Issue Created", "color": "#ff0000",
            "title": str(issue.id) + " - " + item.account + " - " + item.name,
            "fields": [
            {"title": "Score", "value": issue.score, "short": True },
            {"title": "Technology","value": str(item.index),"short": True },
            {"title": "Issue", "value": issue.issue, "short": False },
            {"title": "Notes", "value": issue.notes, "short": False }],
            "title_link": server_url + "/#/items/-/" + str(item.index) + "/-/-/" + item.name + "/-/-/-/-/-/1/25",
            "fallback": "New Security Monkey Notification!",
            "footer": "Security Monkey Team"}]

            postMessage(attachments)

        for issue in item.confirmed_fixed_issues:
            if issue.justified:
                attachments = [{"author_name": "Auditor - Reporting on Issue Fixed", "color": "#00ff00",
                        "title": str(issue.id) + " - " + item.account + " - " + item.name,
                        "fields": [
                                {"title": "Score", "value": issue.score, "short": True },
                                {"title": "Technology","value": str(item.index),"short": True },
                                {"title": "Issue", "value": issue.issue, "short": False },
                                {"title": "Justification", "value": issue.justification + " - " + issue.user.email, "short": False } ],
                        "title_link": server_url + "/#/items/-/" + str(item.index) + "/-/-/" + item.name + "/-/-/-/-/-/1/25",
                        "fallback": "New Security Monkey Notification!",
                        "footer": "Security Monkey Team"}]
            else:
                attachments = [{"author_name": "Auditor - Reporting on Issue Fixed", "color": "#00ff00",
                        "title": str(issue.id) + " - " + item.account + " - " + item.name,
                        "fields": [
                                {"title": "Score", "value": issue.score, "short": True },
                                {"title": "Technology","value": str(item.index),"short": True },
                                {"title": "Issue", "value": issue.issue, "short": False }],
                        "title_link": server_url + "/#/items/-/" + str(item.index) + "/-/-/" + item.name + "/-/-/-/-/-/1/25",
                        "fallback": "New Security Monkey Notification!",
                        "footer": "Security Monkey Team"}]

            postMessage(attachments)

#UNCOMMENT ALL POSTMESSAGE FUNCTIONS WHEN YOUR SLACKCLIENT IS SETUP
def report_watcher_changes(watcher):
    for item in watcher.created_items:
        attachments = [{"author_name": "Watcher - Created Items", "color": "#00ffff",
                "title": str(item.index) + " - " + item.account + " - " + item.name,
                "fields": [
                {"title": "Name", "value": item.name, "short": True },
                {"title": "Technology","value": str(item.index),"short": True }],
                "title_link": server_url + "/#/items/-/" + str(item.index) + "/-/-/" + item.name + "/-/-/-/-/-/1/25",
                "fallback": "New Security Monkey Notification!",
                "footer": "Security Monkey Team"}]

        postMessage(attachments)

    for item in watcher.deleted_items:
        attachments = [{"author_name": "Watcher - Deleted Items", "color": "#000000",
                "title": str(item.index) + " - " + item.account + " - " + item.name,
                "fields": [
                {"title": "Name", "value": item.name, "short": True },
                {"title": "Technology","value": str(item.index),"short": True }],
                "title_link": server_url + "/#/items/-/" + str(item.index) + "/-/-/" + item.name + "/-/-/-/-/-/1/25",
                "fallback": "New Security Monkey Notification!",
                "footer": "Security Monkey Team"}]

        postMessage(attachments)

    for item in watcher.changed_items:
        attachments = [{"author_name": "Watcher - Changed Items", "color": "#ffff00",
                "title": item.index + " - " + item.account + " - " + item.name,
                "fields": [
                {"title": "Name", "value": item.name, "short": True },
                {"title": "Technology","value": item.index,"short": True }],
                "title_link": server_url + "/#/items/-/" + item.index + "/-/-/" + item.name + "/-/-/-/-/-/1/25",
                "fallback": "New Security Monkey Notification!",
                "footer": "Security Monkey Team"}]

        postMessage(attachments)