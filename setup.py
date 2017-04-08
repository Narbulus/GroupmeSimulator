import json, requests, os, sys, util, load_messages, shutil

# Load the list of groups the user is a member of
print("Loading user group information")
groups = util.get_rest('groups')
if groups is None:
    print("Unable to load user's group information")
    sys.exit(1)

for i, group in enumerate(groups):
    print('\t' + str(i + 1) + '. ' + group["name"])

num = int(input("Group to simulate [1-" + str(len(groups)) + "]: "))
while num < 1 or num > len(groups):
    print("Number must be between 1 and " + str(len(groups)))
    num = int(input("Group to simulate [1-" + str(len(groups)) + "]: "))
group = groups[num - 1]

print("'" + group["name"] + "' selected")
new_config = util.CONFIG
new_config["group_id"] = group["id"]
util.write_config(new_config)
print("Group ID written to config")

print("Removing old group information")
if os.path.exists('members'):
    shutil.rmtree('members')
if os.path.exists('eventlog'):
    os.remove('eventlog')
if os.path.exists('bots.json'):
    os.remove('bots.json')
if os.path.exists('lastrun.json'):
    os.remove('lastrun.json')
os.mkdir("members")
print("Done cleaning old information")

print("Loading group information for first run")
load_messages.main("reset")
print("Done loading group information")

print("Setup Complete")
