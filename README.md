# TFDPostBot
## Summary
This is a script to post updates to Mastodon while attending Tech Field Day events. It's very, very simple, but this will help keep a consistent format to my
updates while an event is going on.

## Files
### main.py
This is the main Python script to run. It will load up the credentials, event data, presenter data, and some
message text and send a consistently-formatted update to my Mastodon account.

### creds.yml
A YAML file with the URL and token for Mastodon access.

`token`: The token the Mastodon server gave me.

`base_url` The hostname of the Mastodon server (e.g., `mastodon.social`)

### event.yml
A YAML file with the event data.

`name`: The name of the event (e.g., `Network Field Day 38383`, `Tech Field Day 9499`)

`tags`: A list of tags to include in each update

### presenter.yml
A YAML file with information on the current presenter.

`name`: The name of the presenting company (e.g., `Cisco', `Juniper`)

`reference`: The online presence of the presenter (e.g., `cisco@twitter.com`, `aconaway@masto.ai`) # This needs some work!

### msg.txt
A text file with the next update. This will be overwritten for each update.
