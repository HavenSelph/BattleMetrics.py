from __future__ import annotations
from dataclasses import dataclass
import json
from .identifier import Identifier


@dataclass
class BanRelationship:
    server_id: str
    organization_id: str
    player_id: str
    user_id: str
    ban_list_id: str

    def as_dict(self):
        return {
            "server": {
                "data": {
                    "type": "server",
                    "id": self.server_id
                }
            },
            "organization": {
                "data": {
                    "type": "organization",
                    "id": self.organization_id
                }
            },
            "player": {
                "data": {
                    "type": "player",
                    "id": self.player_id
                }
            },
            "user": {
                "data": {
                    "type": "user",
                    "id": self.user_id
                }
            },
            "banList": {
                "data": {
                    "type": "banList",
                    "id": self.ban_list_id
                }
            }
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            server_id=data["server"]["data"]["id"] if "server" in data else None,
            organization_id=data["organization"]["data"]["id"] if "organization" in data else None,
            player_id=data["player"]["data"]["id"] if "player" in data else None,
            user_id=data["user"]["data"]["id"] if "user" in data else None,
            ban_list_id=data["banList"]["data"]["id"] if "banList" in data else None,
        )


@dataclass
class Ban:
    id: [str, str]  # id, uid
    meta_player_name: str
    timestamp: str
    expires: str
    reason: str
    note: str
    identifiers: list[Identifier]
    auto_add_enabled: bool
    organization_wide: bool
    relationship: BanRelationship

    def as_dict(self):
        return {
            "type": "ban",
            "id": self.id[0],
            "meta": {"player": self.meta_player_name},
            "attributes": {
                "id": self.id[0],
                "uid": self.id[1],
                "timestamp": self.timestamp,
                "reason": self.reason,
                "note": self.note,
                "identifiers": [ident.as_dict() for ident in self.identifiers],
                "expires": self.expires,
                "autoAddEnabled": self.auto_add_enabled,
                "nativeEnabled": None,
                "orgWide": self.organization_wide,
            },
            "relationships": self.relationship.as_dict(),
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=(data["id"], data["attributes"]["uid"]),
            meta_player_name=data["meta"]["player"] if "meta" in data else None,
            timestamp=data["attributes"]["timestamp"],
            expires=data["attributes"]["expires"],
            reason=data["attributes"]["reason"],
            note=data["attributes"]["note"],
            identifiers=[Identifier.from_dict(ident) for ident in data["attributes"]["identifiers"]],
            auto_add_enabled=data["attributes"]["autoAddEnabled"],
            organization_wide=data["attributes"]["orgWide"],
            relationship=BanRelationship.from_dict(data["relationships"]),
        )
