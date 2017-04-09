import json, datetime, sys, markovify, random
import os.path
from collections import defaultdict

SYS_KEYMAP = {
    'ADDED': " added ",
    'NAME_CHANGE': ' changed name to ',
    'AVATAR_CHANGE': " changed the group's avatar",
    'REMOVED': " removed ",
    'LEFT': " has left the group",
    'REJOIN': " has rejoined the group",
    'GROUP_NAME_CHANGE': " changed the group's name to ",
}

# load user information
def load_user_info(group_id):
    info_file = open("groups/" + group_id + '/lastrun.json', 'r')
    info = json.loads(info_file.read())
    info_file.close()
    user_info = info['users']
    return user_info

# helper functions 
def last_nickname(user_id, user_info):
    return user_info[user_id]['names'][-1]

def id_from_nickname(nickname, user_info):
    for u_id, u_info in user_info.items():
        if nickname in u_info['names']:
            return u_id
    print('ID for nickname \"' + nickname + '\" not found')
    return None

def generate_message(user_id, models):
    model = models[user_id]
    return model.make_sentence(tries=1000)

def parse_system_event(text, keymap):
    for keycode, keyword in keymap.items():
        if keyword in text:
            user = text.split(keyword)[0]
            return keycode, user
    print("Unable to parse system event")
    return None, None

# train a model for each user and a base model
def train_user_models(group_id, user_info):
    group_dir = "groups/" + group_id
    models = {}
    all_lines = ''
    for u_id, u_info in user_info.items():
        print("Training model for " + u_info['names'][-1] + " | ID: " + u_id)
        if os.path.isfile(group_dir + '/members/' + u_id):
            msg_file = open(group_dir + '/members/' + u_id, 'r')
            text = msg_file.read()
            all_lines = all_lines + '\n' + text
            model = markovify.NewlineText(text)
            models[u_id] = model
            msg_file.close()
        else:
            print("No messages found")
    # train a model on all users combined
    base_model = markovify.NewlineText(all_lines)
    return models, base_model

def train_event_model(group_id, user_info):
    # train on the event chain
    event_file = open("groups/" + group_id + '/eventlog', 'r')
    events = []
    event_counts = defaultdict(lambda: defaultdict(int))
    event_totals = defaultdict(int)
    post_total = 0

    for line in event_file.readlines():
        event = json.loads(line)
        if event['user_id'] == 'system':
            event_type, user_name = parse_system_event(event['text'], SYS_KEYMAP)
            user = id_from_nickname(user_name, user_info)
            # randomly choose someone if we can't figure out their nickname
            if user is None:
                user = random.choice(list(user_info.keys()))
        else:
            event_type = 'POST'
            user = event['user_id']
        event_counts[event_type][user] += 1
        event_totals[event_type] += 1
        events.append(event_type + " " + user)
        post_total += 1
        
    event_corpus = ""
    for event in events:
        event_corpus += event + ' '
        if (random.randint(0, 10) == 5):
            event_corpus += "\n"

    return markovify.NewlineText(event_corpus)

def write_model(filename, model):
    outfile = open(filename, 'w')
    outfile.write(model.to_json())
    outfile.close()

def load_model(filename):
    f = open(filename, 'r')
    model = markovify.Text.from_json(f.read())
    f.close()
    return model

def gen_events(event_model, models, user_info):
    event_string = event_model.make_sentence()
    event_tokens = event_string.split(' ')
    for t in range(0, len(event_tokens) - 1, 2):
        event_type = event_tokens[t]
        event_user = event_tokens[t + 1]
        if event_type == "POST":
            print(last_nickname(event_user, user_info) + ":")
            print(generate_message(event_user, models))
        else:
            print(">>>>>>>SYSTEM EVENT")
            print(last_nickname(event_user, user_info) + SYS_KEYMAP[event_type])
