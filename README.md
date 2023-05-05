# BattleMetrics.py
Super easy to use (hopefully) API wrapper for [BattleMetics](https://www.battlemetrics.com)


Currently VERY experimental, just a couple dataclasses for Identifiers, Bans, Servers, and a Client for simple requests using these. Will be worked on heavily moving into the future. In its current form, the following is possible, and very friendly to do:
```py
from rich import print
from Battlemetrics.client import Client
from env import envs  # This is a custom file to load variables from a ".env" file.


client = Client(api_key=envs["api_key"], server_id=envs["server_id"])
print(client.server.players, "out of", client.server.max_players, "players are online.")
bans = client.get_all_bans()
ban = bans[3]
print(ban.reason)
server = client.get_server_by_id(bans[3].relationship.server_id)[0]
print(server.name)
print(server.relationship)
print()
```
Output (I have removed private information, but it is all there):
```
95 out of 100 players are online.
Rule 1.3 - Griefing | {{timeLeft}} | Appeal at discord.gg/PRIVATESERVERNAME
PRIVATESERVERNAME Discord.gg/PRIVATESERVERNAME
ServerRelationship(game='squad', organization='PRIVATEORGID')
```


You're fine to collaborate with me, but please include a description of changes in your pull request, and please do not touch code that doesn't relate to your change. Instead, open a second pull request for those changes. Thank you.
