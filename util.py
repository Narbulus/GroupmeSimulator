import json, requests, sys

URL='https://api.groupme.com/v3'

# Attempt to load the config file
try:
    config_file = open('config.json')
except IOError:
    print("Cannot open config file, exiting")
    sys.exit(1)

CONFIG = json.loads(config_file.read())
config_file.close()

if not 'token' in CONFIG:
    print("Invalig config file, see readme")
    sys.exit(1)

TOKEN = CONFIG["token"]

# Re writes the config file with the given config dict
def write_config(config):
    if not 'token' in config:
        print("Config needs a 'token' field")
        return
    config_file = open('config.json', 'w')
    config_file.write(json.dumps(config))
    config_file.close()
    
# hit a get rest endpoint with the given params,
# returning the result as a json object
def get_rest(endpoint, params={}):
    params['token'] = TOKEN
    res = requests.get(URL + '/' + endpoint, params=params)
    if (res.status_code == 200):
        return json.loads(res.text)['response']
    else:
        print(res.text)
        return None

# hit a post rest endpoint with the given params,
# returning the result as a json object
def post_rest(endpoint, data={}, params={}, headers={}):
    params['token'] = TOKEN
    res = requests.post(URL + '/' + endpoint, data=json.dumps(data), params=params, headers=headers)
    print(res.text)
    if (res.status_code == 200 or res.status_code == 201):
        return json.loads(res.text)['response']
    else:
        return None


