from __future__ import annotations
from dataclasses import dataclass
import json


@dataclass
class Identifier:
    """
    Represents a BattleMetrics identifier.

    :param:type: str
        The type of the identifier.
            one of: "steamID", "BEGUID",
    :param:id: (int, str)
        The ID of the identifier.
            (int) for ID and str for UUID/SteamID64
    :param:private: bool
        Whether the identifier is private.
    :param:last_seen: str
        The last time the identifier was seen.
    :param:meta: any
        The metadata of the identifier, if any.
    :param:raw: dict
        The raw dict of the identifier.

    """
    id: (int, str)
    private: bool
    last_seen: str
    meta: any
    type: str

    def as_dict(self):
        return {
            "id": self.id[0],
            "type": self.type,
            "identifier": self.id[1],
            "private": self.private,
            "metadata": self.meta.as_dict() if self.meta else None,
            "lastSeen": self.last_seen,
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, data: dict):
        _id = data.get("id", None) or data.get("identifier", None)
        _uid = data.get("identifier", None) or id
        ident = cls(
            id=(_id, _uid),
            type=data["type"],
            private=data.get("private", False),
            meta=data.get("metadata", None),
            last_seen=data.get("lastSeen", None),
        )
        match data["type"]:  # At the moment, only steamID is supported.
            case "steamID":
                ident.meta = SteamProfile.from_dict(ident.meta) if ident.meta else None
        return ident


@dataclass
class SteamProfile:
    id_64: int
    persona_name: str
    persona_state: int
    persona_state_flags: int
    primary_clan_id: int
    time_created: int
    community_visibility_state: int
    profile_state: int
    comment_permission: int
    profile_url: str
    avatar: str
    avatar_medium: str
    avatar_full: str
    avatar_hash: str

    community_banned: bool
    vac_banned: bool
    number_of_vac_bans: int
    days_since_last_ban: int
    number_of_game_bans: int
    economy_ban: str

    game_info_last_updated: str

    def as_dict(self):
        return {
            "profile": {
                "steamid": self.id_64,
                "communityvisibilitystate": self.community_visibility_state,
                "profilestate": self.profile_state,
                "personaname": self.persona_name,
                "commentpermission": self.comment_permission,
                "profileurl": self.profile_url,
                "avatar": self.avatar,
                "avatarmedium": self.avatar_medium,
                "avatarfull": self.avatar_full,
                "avatarhash": self.avatar_hash,
                "personastate": self.persona_state,
                "primaryclanid": self.primary_clan_id,
                "timecreated": self.time_created,
                "personastateflags": self.persona_state_flags,
            },
            "bans": {
                "SteamId": self.id_64,
                "CommunityBanned": self.community_banned,
                "VACBanned": self.vac_banned,
                "NumberOfVACBans": self.number_of_vac_bans,
                "DaysSinceLastBan": self.days_since_last_ban,
                "NumberOfGameBans": self.number_of_game_bans,
                "EconomyBan": self.economy_ban,
            },
            "gameInfo": {
                "steamid": self.id_64,
                "lastCheck": self.game_info_last_updated,
            }
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def from_dict(cls, data: dict) -> SteamProfile:
        profile, bans, gameinfo = data["profile"], data["bans"], data.get("gameInfo", None)
        return cls(
            id_64=profile["steamid"],
            persona_name=profile["personaname"],
            persona_state=profile.get("personastate", None),
            persona_state_flags=profile.get("personastateflags", None),
            primary_clan_id=profile.get("primaryclanid", None),
            time_created=profile.get("timecreated", None),
            community_visibility_state=profile.get("communityvisibilitystate", None),
            profile_state=profile.get("profilestate", None),
            comment_permission=profile.get("commentpermission", None),
            profile_url=profile["profileurl"],
            avatar=profile["avatar"],
            avatar_medium=profile["avatarmedium"],
            avatar_full=profile["avatarfull"],
            avatar_hash=profile["avatarhash"],
            community_banned=bans["CommunityBanned"],
            vac_banned=bans["VACBanned"],
            number_of_vac_bans=bans["NumberOfVACBans"],
            days_since_last_ban=bans["DaysSinceLastBan"],
            number_of_game_bans=bans["NumberOfGameBans"],
            economy_ban=bans["EconomyBan"],
            game_info_last_updated=gameinfo["lastCheck"] if gameinfo else None,
        )
