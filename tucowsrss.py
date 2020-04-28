import requests
import pymsteams
from xml.etree import ElementTree

#Link up with a webhook from Teams - https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using#setting-up-a-custom-incoming-webhook
myTeamsMessage = pymsteams.connectorcard("<webhook URL>")

# An array of any keywords to match in the <title>
KEYWORDS = ["email", "cluster"]

# Get the HTTP GET Response from the URL
response = requests.get("https://www.opensrsstatus.com/history.rss")

# Format the response body from a string into the ElementTree
xml_body = ElementTree.fromstring(response.content)

# This will leave the <channel> object as the top-level, so we can just dig into the first element
channel = xml_body[0]

# Loop over ever block inside the <channel> object
for item in channel:
#Find any <item> inside the <channel>
    if item.tag == "item":
        # Loop over each block inside the <item> we found
        for child in item:
            title = item[0].text
            for keyword in KEYWORDS:
                if keyword in title:
                    #Array for items in the body, this isn't clean but the formatting should not change
                    description = item[1].text
                    pubDate = item[2].text
                    link = item[3].text
                    #Post message into Teams
                    message = f"Title : {title}\n description: {description}\n Date posted: {pubDate} <br> <a href={link}>{link}</a>"
                    myTeamsMessage.text(message)
                    myTeamsMessage.send()
