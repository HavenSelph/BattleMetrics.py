import requests
import json
from urllib.parse import urlparse, parse_qs
from .server import Server
from .ban import Ban


class Client:
    __API__ = "https://api.battlemetrics.com"

    def __init__(self, api_key: str, server_id: str, game: str="squad"):
        """
        A client for the Battlemetrics API.
        """
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.server_id = server_id
        self.server, self.server_raw = self.get_server_by_id(self.server_id)

    def get_server_by_id(self, server_id: str) -> (Server, dict):
        """
        Get the server from the Battlemetrics API.
        """
        r = requests.get(f"{Client.__API__}/servers/{server_id}", headers=self.headers)
        if r.status_code != 200:
            print(r.text)
            raise Exception(f"Failed to get server from Battlemetrics API. Status code: {r.status_code}")
        server = Server.from_dict(json.loads(r.text))
        return server, json.loads(r.text)

    def get_all_bans(self):
        """
        Get the bans from the Battlemetrics API.
        """
        bans = []
        url = f"{Client.__API__}/bans"
        params = {"filter[server]": self.server_id, "page[rel]": "next", "page[size]": "100", "sort": "-timestamp"}
        while True:
            r = requests.get(url, headers=self.headers, params=params)
            if r.status_code != 200:
                raise Exception(f"Failed to get bans from Battlemetrics API. Status code: {r.status_code}")
            r = json.loads(r.text)

            [bans.append(Ban.from_dict(ban)) for ban in r["data"]]
            if "next" in r["links"].keys():
                u = urlparse(r["links"]["next"]).query
                u = parse_qs(u)
                params = u
            else:
                break
        return bans







