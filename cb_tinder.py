"""Use Cleverbot to reply to messages"""
import datetime
import time

import pynder
import fb_auth
import messaging
from cleverbot import Cleverbot


def main():
    """Main method"""
    session = fb_auth.get_tinder_session()

    # All messages before start_time will be ignored
    #start_time = datetime.datetime.strptime('Jan 1 2017  1:00AM', '%b %d %Y %I:%M%p')
    start_time = datetime.datetime.utcnow()

    # Run this in a loop
    bots_map = {}
    while True:
        try:
            # Get new unreplied messages
            unreplied_messages = messaging.get_unreplied_messages(session, start_time)
            # Use bot to reply to unreplied messages
            for message_tuple in unreplied_messages:
                the_message = message_tuple[0]
                the_match = message_tuple[1]
                bot_reply = get_bot_reply(bots_map, the_match.user, the_message.body)
                print bot_reply
                print the_match.message(bot_reply)
        except pynder.errors.RequestError as request_error:
            print request_error.message
            if request_error.message == 401:
                # Re-auth if getting 401
                print "Re-auth"
                session = fb_auth.get_tinder_session()
        # Wait a while before polling
        time.sleep(30)

    print "Exiting"

def get_bot_reply(bots_map, user, message_body):
    """Gets the bot's reply for the user's message"""
    # Encode message to UTF-8
    message_body = message_body.encode('utf-8')
    bot = get_bot_for_user(bots_map, user)
    reply = bot.ask(message_body)
    return reply

def get_bot_for_user(bots_map, user):
    """Gets the bot created for the user"""
    if not bots_map.has_key(user.id):
        print "Creating new CB session for", user.id, user.name, user.jobs
        bots_map[user.id] = Cleverbot("tinder-cb")
    return bots_map[user.id]

if __name__ == "__main__":
    main()
