# import mastodon
from mastodon import Mastodon
import yaml

with open("msg.txt") as file:
    toot_text = file.read()

with open("event.yml") as file:
    event_data = yaml.safe_load(file)

with open("presenter.yml") as file:
    presenter_data = yaml.safe_load(file)

with open("creds.yml") as file:
    creds_data = yaml.safe_load(file)

presenter_text = f"{presenter_data['name']} is at {presenter_data['reference']}"

tag_list = ""
for tag in event_data['tags']:
    tag_list = f"{tag_list}#{tag} "

msg = f"{toot_text}\n\n{presenter_text}\n{tag_list}"

print(msg)
# masto_conn = Mastodon(access_token=creds_data['token'], api_base_url=creds_data['base_url'])
#
# masto_conn.toot(msg)