"""Messaging functionalities of tinder bot"""
import datetime

def get_unreplied_messages(session, since):
    """Gets the messages that are sent by the match, but not replied by me yet
    Returns an array of (message, match) tuples"""
    print "Getting unreplied messages", datetime.datetime.now()
    #since_str = since.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    unreplied_messages = []
    matches = session.matches()
    #matches = session.matches(since_str)
    my_profile_id = session.profile.id
    for match in matches:
        match_messages = match.messages
        if len(match_messages) == 0:
            continue
        message = match_messages[-1]
        sent_time_utc = message.sent.replace(tzinfo=None)
        if message.to.id == my_profile_id and sent_time_utc > since:
            print message
            unreplied_messages.append((message, match))
    return unreplied_messages
