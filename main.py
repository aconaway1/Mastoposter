"""
Posts a status update to Mastodon using a jinja2 template and data taken from YAML files.

This script is targeted to be used during streaming events where lots of posts are made.
The idea is that each post is consistent and includes accurate tags and links as well
as your comments.

NOTE: I am a network engineer and not a developer. I think my code is improving, but, 
for the love of $deity, do not assume that the way I do it is best practice!
"""
import argparse
import logging
from jinja2 import Template
import yaml
from mastodon import Mastodon


VERSION = 1.1
TEMPLATE_FILE = "post_template.j2"
LOG_FILE = "output.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def init_args() -> argparse.ArgumentParser:
    """
    Initializes the CLI arguments
    
    Returns:
        argparse.ArgumentParser - The argparse parser to use later
    """
    parser = argparse.ArgumentParser(
        description="Post a message to Mastodon during a streaming event",
    )
    parser.add_argument(
        "-c", "--content-warning",
        help="Add a content warning to this post",
    )
    parser.add_argument(
        "-t", "--ignore-template",
        action="store_true",
        help="Ignore the template and post as raw message",
    )
    parser.add_argument(
        "-p", "--ignore-presenter",
        action="store_true",
        help="Do not add the presenter info to the message",
    )
    parser.add_argument(
        "-e", "--ignore-event",
        action="store_true",
        help="Do not add the event info to the message",
    )
    parser.add_argument(
        "-o", "--offline",
        action="store_true",
        help="Don't actually send the message to Mastodon but do everything else."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} {VERSION}"
    )
    parser.add_argument('message')
    return parser


def set_logging() -> None:
    """
    Sets up the logging location, format, and level
    """
    logging.basicConfig(
        filename=LOG_FILE,
        format=LOG_FORMAT,
        level=logging.INFO
    )


def log_summary(given_cw_text: str, given_arg: argparse.Namespace, given_msg: str) -> None:
    """
    Logs a summary of the toot to file
    """
    logging.info("Summary of the toot:")
    logging.info("CW: %s", given_cw_text)
    logging.info("ignore_template: %s", given_arg.ignore_template)
    logging.info("ignore_presenter %s", given_arg.ignore_presenter)
    logging.info("ignore_event %s", given_arg.ignore_event)
    logging.info("arg_message %s", given_arg.message)
    logging.info("message to be sent:\n%s", given_msg)
    print(f"{given_msg}")

def main():
    """
    Do stuff
    """
    set_logging()
    parser = init_args()
    arguments = parser.parse_args()
    cw_text = ""
    msg_data = {}
    if arguments.content_warning:
        logging.info("Adding a content warning to this message as \"%s\"",
                     arguments.content_warning)
        cw_text = arguments.content_warning

    msg_data['msg'] = arguments.message
    logging.info("Trying to post with this message:\n%s", msg_data['msg'])

    if not arguments.ignore_event:
        with open("event.yml", encoding="UTF-8") as file:
            msg_data['event'] = yaml.safe_load(file)
            logging.info("Got the event data.")
    else:
        logging.info("Ignoring the event info from file.")

    if not arguments.ignore_presenter:
        with open("presenter.yml", encoding="UTF-8") as file:
            msg_data['presenter'] = yaml.safe_load(file)
            logging.debug("Got the presenter data.")
            if "cw" in msg_data['presenter']:
                if len(cw_text) > 0:
                    cw_text = cw_text + f" - {msg_data['presenter']['cw']}"
                else:
                    cw_text = msg_data['presenter']['cw']

    if not arguments.ignore_template:
        with open(TEMPLATE_FILE, encoding="UTF-8") as file:
            template = Template(file.read())
        rendered_msg = template.render(msg_data)
        logging.debug("Rendered the template:\n---\n%s\n---", rendered_msg)
    else:
        rendered_msg = arguments.message

    log_summary(given_cw_text=cw_text, given_arg=arguments, given_msg=rendered_msg)

    with open("creds.yml", encoding="UTF-8") as file:
        creds_data = yaml.safe_load(file)
        logging.debug("Got the cred data.")

    if not arguments.offline:
        masto_conn = Mastodon(access_token=creds_data['token'], api_base_url=creds_data['base_url'])
        logging.debug("The Mastodon connection: %s", masto_conn)

        toot_result = masto_conn.status_post(rendered_msg, spoiler_text=cw_text)
        logging.debug(toot_result)
        logging.info("Posted message %s", toot_result['id'])
    else:
        logging.info("Didn't not post to Mastodon since the -o flag was given")


if __name__ == "__main__":
    main()
