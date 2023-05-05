from __future__ import annotations
from dataclasses import dataclass
import json


@dataclass
class Server:
    """
    Dataclass for a server object from the Battlemetrics API.

    WARNING: This is not a complete dataclass. It is missing some fields.
    You will lose some game-specific data if you use this dataclass.

    """
    id: str
    name: str
    address: str
    ip: str
    port: int
    players: int
    max_players: int
    rank: int
    location: [float, float]
    status: str
    details: dict
    private: bool
    created_at: str
    updated_at: str
    port_query: int
    country: str
    query_status: str
    relationship: ServerRelationship

    def as_dict(self):
        return {
            "data": {
                "type": "server",
                "id": self.id,
                "attributes": {
                    "id": self.id,
                    "name": self.name,
                    "address": self.address,
                    "ip": self.ip,
                    "port": self.port,
                    "players": self.players,
                    "maxPlayers": self.max_players,
                    "rank": self.rank,
                    "location": self.location,
                    "status": self.status,
                    "details": self.details,
                    "private": self.private,
                    "createdAt": self.created_at,
                    "updatedAt": self.updated_at,
                    "portQuery": self.port_query,
                    "country": self.country,
                    "queryStatus": self.query_status,
                }
            },
            "relationships": self.relationship.as_dict(),
            "included": []
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, data: dict):

        inner, attributes = data["data"], data["data"]["attributes"]
        return cls(
            id=inner["id"],
            name=attributes["name"],
            address=attributes["address"],
            ip=attributes["ip"],
            port=attributes["port"],
            players=attributes["players"],
            max_players=attributes["maxPlayers"],
            rank=attributes["rank"],
            location=attributes["location"],
            status=attributes["status"],
            details=attributes["details"],
            private=attributes["private"],
            created_at=attributes["createdAt"],
            updated_at=attributes["updatedAt"],
            port_query=attributes["portQuery"],
            country=attributes["country"],
            query_status=attributes["queryStatus"],
            relationship=ServerRelationship.from_dict(inner["relationships"])
        )


@dataclass
class ServerRelationship:
    game: str
    organization: str

    def as_dict(self):
        return {
            "game": {
                "data": {
                    "type": "game",
                    "id": self.game
                }
            },
            "organization": {
                "data": {
                    "type": "organization",
                    "id": self.organization
                }
            }
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            game=data["game"]["data"]["id"],
            organization=data["organization"]["data"]["id"],
        )


# NOT SUPPORTED YET
# Need a clean way to handle game-specific data
#
# @dataclass
# class SquadServer(Server):
#     details: SquadServerDetails
#     rcon_active: bool
#     metadata: None  # Not supported yet
#     rcon_status: str
#     rcon_last_connected: str
#     rcon_disconnected: any
#
#
# @dataclass
# class SquadServerDetails:
#     map: str
#     game_mode: str
#     version: str
#     secure: bool
#     licensed: bool
#     license_id: str
#     num_public_connections: int
#     num_private_connections: int
#     squad_player_reserve_count: int
#     squad_play_time: int
#     squad_public_queue_limit: int
#     squad_public_queue: int
#     squad_reserved_queue: int
#     squad_team_one: str
#     squad_team_two: str
#     modded: bool
#     server_steam_id: str
#
