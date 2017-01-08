"""Cleverbot powered Tinder!"""
import datetime
import time

import pynder
import fb_auth
from cleverbot import Cleverbot


def main():
    """Main method"""
    logged_in = False
    while not logged_in:
        fb_token = fb_auth.get_access_token()
        try:
            print "Creating Tinder session..."
            session = pynder.Session(fb_token)
            print "Connected to Tinder!"
            fb_auth.save_access_token_to_file(fb_token)
            logged_in = True
        except pynder.errors.RequestError as request_error:
            print request_error.message
            fb_auth.delete_access_token_file()

    # Run this in a loop
    bots_map = {}
    while True:
        since = datetime.datetime.utcnow()
        unreplied_messages = get_unreplied_messages(session, since)
        # Use bot to reply to unreplied messages
        for message_tuple in unreplied_messages:
            the_message = message_tuple[0]
            the_match = message_tuple[1]
            bot_reply = get_bot_reply(bots_map, the_match.user, the_message.body)
            print bot_reply
            print the_match.message(bot_reply)
        # Wait a while before polling so that we don't get banned by Tinder
        time.sleep(10)

    print "Exiting"

def get_bot_reply(bots_map, user, message_body):
    """Gets the bot's reply for the user's message"""
    bot = get_bot_for_user(bots_map, user)
    reply = bot.ask(message_body)
    return reply

def get_bot_for_user(bots_map, user):
    """Gets the bot created for the user"""
    if not bots_map.has_key(user.id):
        print "Creating new CB session for", user.id, user.name, user.jobs
        bots_map[user.id] = Cleverbot()
    return bots_map[user.id]

def get_unreplied_messages(session, since):
    """Gets the messages that are sent by the match, but not replied by me yet
    Returns an array of (message, match) tuples"""
    since_str = since.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    unreplied_messages = []
    #matches = session.matches()
    matches = session.matches(since_str)
    my_profile = session.profile
    for match in matches:
        match_messages = match.messages
        if len(match_messages) == 0:
            continue
        last_message = match_messages[-1]
        if last_message.to.id == my_profile.id:
            print last_message
            unreplied_messages.append((last_message, match))
    return unreplied_messages

if __name__ == "__main__":
    main()
