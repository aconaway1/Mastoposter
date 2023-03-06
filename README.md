# TFD-Poster
## Summary
This is a script to post updates to Mastodon while attending Tech Field Day events. It's very, very simple, but this will help keep a consistent format to my
updates while an event is going on.

## Usage

`python main.py "YOUR MESSAGE HERE"`

You can change the format of the update by modifying the `post_template.j2` file.

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

`tags`: A list of tags to include in each update (e.g., `NFD38383`, `TFD9499`)

### presenter.yml
A YAML file with information on the current presenter.

`name`: The name of the presenting company (e.g., `Cisco', `Juniper`)

`where`: The online presence of the presenter (e.g., `cisco@twitter.com`, `aconaway@masto.ai`) # This needs some work!

### post_template.j2
This is the Jinja2 template for the message formatting. This is what you'll update to change the format of the update.

The default format sends the message, the name and online presence of the presenter, and the event hashtags.

`YOUR MESSAGE HERE

Presenter A can be found at @presenterA@twitter.com
#hashtag1 #hashtag2 #hashtag3