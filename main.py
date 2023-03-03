from mastodon import Mastodon
import yaml
import sys
from jinja2 import Template
import logging

TEMPLATE_FILE = "post_template.j2"
LOG_FILE = "output.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def get_spoiler():
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
logging.debug(f"Got the message from CLI: {msg_data['msg']}")

with open(TEMPLATE_FILE) as file:
    template = Template(file.read())
    
with open("event.yml") as file:
    msg_data['event'] = yaml.safe_load(file)
    logging.debug(f"Got the event data.")

with open("presenter.yml") as file:
    msg_data['presenter'] = yaml.safe_load(file)
    logging.debug(f"Got the presenter data.")

with open("creds.yml") as file:
    creds_data = yaml.safe_load(file)
    logging.debug(f"Got the cred data.")
    
msg = template.render(msg_data)
logging.debug(f"Rendered the template:\n---\n{msg}\n---")


masto_conn = Mastodon(access_token=creds_data['token'], api_base_url=creds_data['base_url'])
logging.debug(f"The Mastodon connection: {masto_conn}")

# toot_result = masto_conn.toot(msg)
toot_result = masto_conn.status_post(msg, spoiler_text=get_spoiler())
logging.info(toot_result)
logging.debug(f"Posted message {toot_result['id']}")