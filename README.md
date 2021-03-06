# GroupmeSimulator

Use language models to simulate GroupMe conversations.

## Description
Inspired by the popular subreddit /r/SubredditSimulator, this python program uses the GroupMe REST API to extract
all messages in a group and construct a 'bot' for each member of the group chat. Each bot is trained on all of the
messages its corresponding human has posted in the group chat. The program then creates a simulation group chat
and populates it with bots, allowing the bots to chat amongst themselves.

## Dependencies

* python 3.0
* [markovify](https://github.com/jsvine/markovify) by jsvine
* [requests](http://docs.python-requests.org/en/master/)

## Setup

1. Clone the repository to some directory: `git clone https://github.com/Narbulus/GroupmeSimulator`
2. Create a groupme account if you don't already have one visit the [GroupMe Developers page](https://dev.groupme.com/)
3. Click on the 'Access Token' button on the top right navbar and copy your token.
![developers](https://cloud.githubusercontent.com/assets/10165957/25404825/33f183b4-29f9-11e7-8e83-ff25b329402e.png)
4. Open the `config.json` file in the cloned repository and replace `YOUR_TOKEN_HERE` with the copied token.
5. Run the setup script with `setup.py`

Multiple simulations can be run and managed with the setup script, all saved messages and information will be stored in
the script's working directory.
