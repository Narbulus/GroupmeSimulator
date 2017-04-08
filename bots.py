import json, requests, datetime, sys

config_file = open('config.json')
config = json.loads(config_file.read())
config_file.close()

TOKEN=config['token']
URL='https://api.groupme.com/v3'
GROUP_ID=config['group_id']
BOT_FILE='bots.json'

def bot_exists(user_id, bot_info):
    return user_id in bot_info.keys()

def create_bot(user_id, name, bot_info):
    if user_id in bot_info.keys():
        print("Bot already registered for user " + str(user_id))
        return
    data = {
        "bot": {
            "name": str(name),
            "group_id": str(GROUP_ID),
            "callback_url": "http://104.236.152.196:6000/" + user_id
        }
    }
    headers = { "Content-Type": "application/json" }
    res = post_rest('bots', data=data, headers=headers)
    if res is None:
        print("Bot creating POST request failed")
        return
    bot_info[user_id] = res['bot']
    print("Bot creating successful, bot ID: " + str(res['bot']['bot_id']))

def post_bot(user_id, message, bot_info):
    if not user_id in bot_info.keys():
        print("Bot does not exist for this user")
        return
    bot_id = bot_info[user_id]['bot_id']
    data = {
        'bot_id': bot_id,
        'text': message
    }
    headers = { "Content-Type": "application/json" }
    res = post_rest('bots/post', data=data, headers=headers)
    if res is None:
        print("Bot posting GET request failed")

def load_bot_info():
    bot_file = open(BOT_FILE, 'r')
    bot_info = json.loads(bot_file.read())
    bot_file.close()
    return bot_info

def save_bot_info(bot_info):
    bot_file = open(BOT_FILE, 'w')   
    bot_file.write(json.dumps(bot_info))
    bot_file.close()


