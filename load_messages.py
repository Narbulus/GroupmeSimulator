import json, requests, datetime, sys, os, util
from collections import defaultdict

def main(reset):
    GROUP_ID = util.CONFIG['group_id']
    LAST_RUN = 'lastrun.json'
    EVENT_LOG = 'eventlog'

    # Command line arg to start completely fresh
    # WARNING: Deletes all your old messages
    # (but probably just loads them again)
    RESET = reset == 'reset'
        
    message_params = { 'limit': 100 }
    # reset the last run information if the cmd line arg is set
    # or if this is the first run
    if RESET or not os.path.isfile(LAST_RUN):
        print('Resetting last run information')
        last_info = {}
        seen_messages = 0
        user_info = defaultdict(dict)
        # wipe the old files
        file_mode = 'w'
        param_mode = 'before_id'
        insert_mode = lambda l, x: l.insert(0, x)
    # otherwise just load the last run json file
    else:
        print("Loading last run information")
        last_file = open(LAST_RUN, 'r')
        last_info = json.loads(last_file.read())
        last_file.close()
        last_id = int(last_info['last_id'])
        seen_messages = int(last_info['seen_messages'])
        user_info = last_info['users']
        file_mode = 'a'
        param_mode = 'after_id'
        insert_mode = lambda l, x: l.append(x)
        message_params[param_mode] = last_id

    # keep track of events and name changes
    event_log = []
    user_names = defaultdict(list)
    user_avatars = defaultdict(list)

    # load message count
    message_info = util.get_rest('groups/' + str(GROUP_ID) + '/messages', message_params)
    if not message_info:
        print("No more messages to load")
    else:
        total_messages = int(message_info['count'])
        user_messages = defaultdict(list)
        print("Seen " + str(seen_messages) + ", " + str(total_messages - seen_messages) + " new to load")

        while message_info and seen_messages < total_messages:
            messages = message_info['messages']
            print("Loading messages " + str(seen_messages) + " to " + str(seen_messages + len(messages)))
            for message in messages:
                seen_messages += 1
                last_id = message['id']
                # Don't need to log empty messages
                if message['text'] is None:
                    continue
                user_id, msg_text, avatar_url = message['user_id'], message['text'], message['avatar_url']
                # update user name sets and message lists
                if not message['name'] in user_names[user_id]:
                    insert_mode(user_names[user_id], message['name'])
                if not avatar_url in user_avatars[user_id]:
                    insert_mode(user_avatars[user_id], avatar_url)
                insert_mode(user_messages[user_id], msg_text.lower())
                # Update the event log
                insert_mode(event_log, {
                    "user_id": user_id,
                    "text": msg_text,
                    "created_at": message['created_at'],
                })
            # Load the next batch of messages, going forward or backward
            # based on the reset flag
            message_params[param_mode] = last_id
            message_info = util.get_rest('groups/' + str(GROUP_ID) + '/messages', message_params)

        print("Writing event log")
        event_log_file = open(EVENT_LOG, file_mode)
        for event in event_log:
            event_log_file.write(json.dumps(event) + '\n')
        event_log_file.close()

        print("Writing user message logs")
        for user_id,messages in user_messages.items():
            outfile = open('members/' + user_id, file_mode)
            for m in messages:
                print(m, file=outfile)
            outfile.close()

    # write messages and progress info to file
    print("Writing last run information")
    last_info['last_id'] = last_id
    last_info['seen_messages'] = seen_messages
    last_info['last_timestamp'] = str(datetime.datetime.now())

    # update the user names
    for u_id, u_names in user_names.items():
        # append new names to oldies
        u_names = user_info[u_id].get('names', []) + u_names
        user_info[u_id]['names'] = u_names

    # update avatars
    for u_id, u_avatars in user_avatars.items():
        print(u_avatars)
        if 'avatars' in user_info[u_id]:
            u_avatars = old_avatars + u_avatars
        user_info[u_id]['avatars'] = u_avatars

    last_info['users'] = user_info
    last_file = open(LAST_RUN, 'w')
    last_file.write(json.dumps(last_info))
    last_file.close()

    print("Done")

if __name__ == "__main__":
    main(sys.argv[1])
