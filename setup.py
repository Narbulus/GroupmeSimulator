import json, requests, os, sys, util, load_messages, shutil, simulate

# Load the list of groups the user is a member of
print("Loading user group information")
groups = util.get_rest('groups', params={"per_page": 100})
if groups is None:
    print("Unable to load user's group information")
    sys.exit(1)

sim_ids = map(lambda conf: conf['simulation_id'], util.CONFIG['groups'].values())
sim_ids = list(sim_ids)
groups = list(filter(lambda group: group['id'] not in sim_ids, groups))

for i, group in enumerate(groups):
    print('\t' + str(i + 1) + '. ' + group["name"])

num = int(input("Group to simulate [1-" + str(len(groups)) + "]: "))
while num < 1 or num > len(groups):
    print("Number must be between 1 and " + str(len(groups)))
    num = int(input("Group to simulate [1-" + str(len(groups)) + "]: "))
group = groups[num - 1]
group_id = group["id"]

print("'" + group["name"] + "' selected")
new_config = util.CONFIG
if "groups" in new_config:
    old_groups = new_config["groups"]
else:
    old_groups = {}
if not group_id in old_groups:
    old_groups[group_id] = {"id": group["id"], "name": group["name"]}
new_config["groups"] = old_groups
print("Group ID written to config")

if not "simulation_id" in old_groups[group_id]:
    print("Creating the simulation group")
    data = { "name": group["name"] + " Simulation" }
    headers = { "Content-Type": "application/json" }
    res = util.post_rest('groups', data=data, headers=headers)
    if res is None:
        print("Creating simulation groupme failed")
    else:
        old_groups[group_id]["simulation_id"] = res["id"]

util.write_config(new_config)

if not os.path.exists("groups"):
    os.mkdir("groups")
if not os.path.exists("groups/" + group_id):
    os.mkdir("groups/" + group_id)
    os.mkdir("groups/" + group_id + '/members')

print("Loading group information for first run")
load_messages.main(group_id, "reset")
print("Done loading group information")

print("Setup Complete")
run = input("Would you like to run the simulation? (y/n): ")
if run == 'y':
    simulate.main(group_id)
