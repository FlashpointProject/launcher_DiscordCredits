# Launcher Discord Credits Generator

Generates or updates a previous credits.json from a Discord servers users and roles. Outputs to credits_new.json.

Bot must have View Channel and Send Message permissions.

## Prerequisities

Python 3

Discord.py. Can install via `pip install -r requirements.txt`

## Setup

Make a file `token.txt` and put your Bot token inside it

Put any roles you don't want to credit inside `uncreditedRoles.txt`. Remember that @everyone is a role.

Put any users that should be excluded from the credits inside `uncreditedUsers.txt`.

Put any users that should always be included in the credits (even if they don't have a credited role) inside `creditedUsers.txt`.

Put any roles that you want to be top roles by default inside `topRoles.txt`.

Put any users you want the Bot to run commands for inside `users.txt`

## Running

Start the bot with `python creditsBot.py`

Run the `>run` command inside any channel the bot has access to and wait for its response.

`credits_new.json` will be present in the same directory. `credits.json` will be used as a base to update from if present.