import bots, generate, time, random

user_info = generate.load_user_info()
bot_info = bots.load_bot_info()

models, base_model = generate.train_user_models(user_info)
event_model = generate.train_event_model(user_info)

# create a bot for every user that doesn't have one
for u_id in user_info.keys():
    if not bots.bot_exists(u_id, bot_info):
        name = generate.last_nickname(u_id, user_info)
        bots.create_bot(u_id, name, bot_info)

# save our changes
bots.save_bot_info(bot_info)

def simulate_sequence():
    event_string = event_model.make_sentence()
    event_tokens = event_string.split(' ')
    for t in range(0, len(event_tokens) - 1, 2):
        event_type = event_tokens[t]
        event_user = event_tokens[t + 1]
        if event_type == "POST":
            message = generate.generate_message(event_user, models)
            print("User: " + event_user + " posted:")
            print(message)
            bots.post_bot(event_user, message, bot_info)
        else:
            print(">>>>>>>SYSTEM EVENT")
            print(event_user)
            print(generate.SYS_KEYMAP[event_type])
        time.sleep(5 * random.randrange(1, 30))


while True:
    simulate_sequence()
    time.sleep(60 * random.randrange(1, 3))
