"""
Posts a status update to Mastodon using a jinja2 template and data taken from YAML files.

This script is targeted to be used during event like Tech Field Day where lots of posts are made
so that each post is consistent and includes all the right stuff like links and tags.
"""
import sys
import logging
from jinja2 import Template
import yaml
from mastodon import Mastodon

TEMPLATE_FILE = "post_template.j2"
LOG_FILE = "output.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def get_spoiler():
    """
    Sets the spoiler text for the post based on the `presenter.yml` file

    Returns:
        string: The spoiler text discovered
    """
# Get the spoiler text
    if 'spoiler' not in msg_data['presenter'].keys():
        return None
    return msg_data['presenter']['spoiler']


logging.basicConfig(
    filename=LOG_FILE,
    format=LOG_FORMAT,
    level=logging.DEBUG
)

msg_data = {}

msg_data['msg'] = sys.argv[1]
logging.debug("Got the message from CLI: %s", msg_data['msg'])

with open(TEMPLATE_FILE, encoding="UTF-8") as file:
    template = Template(file.read())

with open("event.yml", encoding="UTF-8") as file:
    msg_data['event'] = yaml.safe_load(file)
    logging.debug("Got the event data.")

with open("presenter.yml", encoding="UTF-8") as file:
    msg_data['presenter'] = yaml.safe_load(file)
    logging.debug("Got the presenter data.")

with open("creds.yml", encoding="UTF-8") as file:
    creds_data = yaml.safe_load(file)
    logging.debug("Got the cred data.")

msg = template.render(msg_data)
logging.debug("Rendered the template:\n---\n%s\n---", msg)


masto_conn = Mastodon(access_token=creds_data['token'], api_base_url=creds_data['base_url'])
logging.debug("The Mastodon connection: %s", masto_conn)

toot_result = masto_conn.status_post(msg, spoiler_text=get_spoiler())
logging.info(toot_result)
logging.debug("Posted message %s", toot_result['id'])
