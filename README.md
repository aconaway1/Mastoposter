# Mastoposter
## Summary
This is a script to post updates to Mastodon while live-Tooting streaming events. It's very, very simple, but this will help keep a consistent format to any updates while an event is going on.

For each event, you update the `event.yml` file with the proper information, and, as each presenter appears, update the `presenter.yml` file with their information. When you Toot, the message will be consistent and accurate based on the Jinja2 template. 

See file section below for details on the YAML files. Pay specific attention to `creds.yml` to make sure you can post to your account.

## Setup
Clone the repo to your machine.

`git clone https://github.com/aconaway1/Mastoposter.git`

CD into the `Mastoposter` directory.

You can use the `requirements.txt` to install what you need. I would suggest doing so in a virtual environment.

`pip install -r requirements.txt`

You need to create a creds file with the proper info to post to your account. Just create the file in the directory and add something like this.

```
token: MYTOKEN
base_url: mymastodon.instance
```

That should be it.

## Usage
### Simple
`python main.py "YOUR MESSAGE HERE"`

You can change the format of the update by modifying the `post_template.j2` file.

### Optional Flags
`-v`: Print the version

`-c` "CONTENT WARNING TEXT": Add an additional content warning. If the presenter has a `cw` directive already (see below), the text of the content warning will be "ARG TEXT - YAML TEXT".

`-o`: Offline mode. Do everything except actually post to Mastodon. This is good for testing a template change and makig sure you have all the Jinja2 spacing correct (which always takes me 8472848 years to fix).

`-t`: Ignore the template. Post the text as-is with no formatting. The content warning from file or argument still applies.

#### Data Flags
These flags are used to *not* send various data to the template. Depending how your template looks, you may want to suppress sending certain data.

`-p`: Ignore the presenter information. The content warning from file will also be ignored.

`-e`: Ignore the event information. That is, don't include the hashtags.

## Files
### main.py
This is the main Python script to run. It will load up the credentials, event data, presenter data, and some
message text and send a consistently-formatted update to your Mastodon account.

### creds.yml
A YAML file with the URL and token for Mastodon access.

`token`: The token the Mastodon server gave you. See the `Development` section of your instance's preferences page for info on that.

`base_url` The hostname of the Mastodon server (e.g., `mastodon.social`)

### event.yml
A YAML file with the event data.

`name`: (NOT USED) The name of the event (e.g., `Streaming Event 2023-8`, `Gaming Super-special Announcement`)

`tags`: A list of tags to include in each update (e.g., `SE2023-8`, `GSSA`)

`url`: (NOT USED) The URL of the event, usually a link to a stream

### presenter.yml
A YAML file with information on the current presenter.

`name`: The name of the presenting company (e.g., `MegaStreamer`, `Big Tech Developer`)

`where`: The online presence of the presenter (e.g., `examplemegastreamer@mastodon.yourmom`)

`cw`: (Optional) If you want all posts to have a content warning, enter some text here.

### post_template.j2
This is the Jinja2 template for the message formatting. This is what you'll update to change the format of the update.

The default format sends the message, the name and online presence of the presenter, and the event hashtags. There will be more functionality later.

```
YOUR MESSAGE HERE

Presenter A can be found at @presenterA@somemastodoninstance

#hashtag1 #hashtag2 #hashtag3
```

## Notes


## Contact

You can contact me via email at aaron@aconaway.com.