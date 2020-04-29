import requests
import pymsteams
import xmltodict


# An array of any keywords to match in the <title>
KEYWORDS = ["email", "cluster"]
# Microsoft Teams webhook URL - https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using#setting-up-a-custom-incoming-webhook
WEBHOOK_URL = ""
# Link to the Status RSS Feed
RSS_FEED_URL = "https://www.opensrsstatus.com/history.rss"


def keyword_in_title(keywords, title):
    for keyword in keywords:
        if keyword in title:
            return True
    return False


def build_message(item):
    title = item["title"]

    description = item["description"]
    pub_date = item["pubDate"]
    link = item["link"]

    return f"Title : {title}<br>\n" + \
           f"Description: {description}<br>\n" + \
           f"Date posted: {pub_date}<br>\n" + \
           f"<a href={link}>{link}</a>"


def post_to_teams(webhook, message):
    teams_connector = pymsteams.connectorcard(webhook)
    teams_connector.text(message)
    teams_connector.send()


if __name__ == "__main__":
    # Get the HTTP GET Response from the URL
    response = requests.get(RSS_FEED_URL)

    # Format the response body from a string into the ElementTree
    xml_body = xmltodict.parse(response.content)

    # Loop over ever <item> inside the <channel> object
    for item in xml_body["rss"]["channel"]["item"]:
        if not keyword_in_title(KEYWORDS, item["title"]):
            continue

        message = build_message(item)
        post_to_teams(WEBHOOK_URL, message)


