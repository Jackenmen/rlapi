import re
from typing import List

__all__ = ("PlayerTitle",)


_SPECIAL_CASED_TITLE_NAMES = {
    # non-standard formatting one-offs for season rewards
    "S10_Grand_Champion": "S10 GRAND CHAMPION",
    "S10_BLIZZARD_WIZARD": "S10 BLIZZARD WIZARD",
    "S10_RNG_CHAMP": "S10 RNG CHAMP",
    "S10_FLOOR_DESTROYER": "S10 FLOOR DESTROYER",
    "S10_DUNK_MASTER": "S10 DUNK MASTER",
    "S10_Supersonic_Legend": "S10 SUPERSONIC LEGEND",
    "S10_ICE_TITAN": "S10 ICE TITAN",
    "S10_RNGENIUS": "S10 RNGENIUS",
    "S10_TILE_ANNIHILATOR": "S10 TILE ANNIHILATOR",
    "S10_LEGENDARY_BALLER": "S10 LEGENDARY BALLER",
    "S26Grand_Champion_Hoops": "S12 DUNK MASTER",
    # special characters
    "90s_Kid": "90'S KID",
    "FOREVER_FASTER": "FOREVER. FASTER.",
    "Gooooal": "GOOOOAL!",
    "FF_TunaNoCrust": "TUNA, NO CRUST",
    "RP2_WallCrawler": "WALL-CRAWLER",
    "RP7_Cross_Platformer": "CROSS-PLATFORMER",
    "RP8_Rockin_Roller": "ROCKIN' ROLLER",
    "RP11_Zero_G": "ZERO-G",
    "RP13_A_Lister": "A-LISTER",
    "RP15_5050_Magician": "50/50 MAGICIAN",
    "RP17_E_Brake_Expert": "E-BRAKE EXPERT",
    "RP17_Choku_Dori_Chief": "CHOKU-DORI CHIEF",
    "SE_Jump_Starter": "JUMP-STARTER",
    "XP_AllStar": "ALL-STAR",
    # splitting issues
    "DreamHack_Champion": "DREAMHACK CHAMPION",
    "PostPartier": "POSTPARTIER",
    "Y2K_Ready": "Y2K READY",
    "FR_4DChessmaster": "4D CHESS MASTER",
    "SE_DEMOgorgon": "DEMOGORGON",
    "SE_Long_Time_Fan": "LONGTIME FAN",
    # name inconsistent with ID
    "Billion_Dollar_Racer": "SIR SUPERSONIC",
    "Headliner": "VOCALIST",
    "RP6_StreetSamurai": "DIRTSIDER",
    "RP12_Major_Creator": "MASTER CRAFTER",
    "SE_Agent007": "00 AGENT",
    "SE_OnlyTheBest": "GOLDEN GOAT",
    "SE_RatRace": "RAT RACER",
    "XP_SupersonicLegend": "LEGENDARY NEMESIS",
    "RLCS_2024_Major_1_Champion": "RLCS 2024 COPENHAGEN MAJOR CHAMPION",
    "RLCS_2024_Major_1_Contender": "RLCS 2024 COPENHAGEN MAJOR CONTENDER",
    "RLCS_2024_Major_2_Champion": "2024 LONDON MAJOR CHAMPION",
    "RLCS_2024_Major_2_Contender": "2024 LONDON MAJOR CONTENDER",
    # one-off tournaments
    "BTS_Champion": "ROCKET LEAGUE SUMMIT CHAMPION",
    "CRL_Spring_Showdown_Champ": "SPRING SHOWDOWN CHAMP",
    "CRL_Spring_Showdown_Elite": "SPRING SHOWDOWN ELITE",
    "GrandSeries_09_Champion": "GRAND SERIES SEASON 9 CHAMPION",
    "GrandSeries_09_Elite": "GRAND SERIES SEASON 9 ELITE",
    "UORL_Champion": "UNIVERSAL OPEN CHAMPION",
    # "Spring" in World Champion is not included in CRL titles from other years
    "CRL_Spring_22_WorldChampion": "CRL 2022 WORLD CHAMPION",
    # CRL_0* titles generally skip the season in their name
    "CRL_02_Contender": "CRL SEASON 2 CONTENDER",
    # for some reason, the year is not included in the ID
    "RLCS_World_Championship_Contender": "RLCS 2024 WORLD CHAMPIONSHIP CONTENDER",
}
_SEASON_REWARD_RE = re.compile(r"S\d+")
_TITLE_CASE_SPLIT_RE = re.compile(r"([A-Z][a-z]+|\d+)")


def _construct_season_reward_title(id_parts: List[str]) -> str:
    season_number = int(id_parts[0][1:])
    season_text = (
        f"S{season_number - 14}" if season_number > 14 else f"SEASON {season_number}"
    )
    mode = id_parts[-1].upper()
    is_gc = id_parts[1].upper() == "GRAND"
    if mode == "RUMBLE":
        if is_gc or mode == "CHAMP":
            return f"{season_text} RNG CHAMP"
        return f"{season_text} RNGENIUS"
    if mode == "CHAMP":
        return f"{season_text} RNG CHAMP"
    if mode == "RNGENIUS":
        return f"{season_text} RNGENIUS"

    if mode == "DROPSHOT":
        if is_gc or mode == "DESTROYER":
            return f"{season_text} FLOOR DESTROYER"
        return f"{season_text} TILE ANNIHILATOR"
    if mode == "DESTROYER":
        return f"{season_text} FLOOR DESTROYER"
    if mode == "ANNIHILATOR":
        return f"{season_text} TILE ANNIHILATOR"

    if mode == "HOOPS":
        if is_gc or mode == "MASTER":
            return f"{season_text} DUNK MASTER"
        return f"{season_text} LEGENDARY BALLER"
    if mode == "MASTER":
        return f"{season_text} DUNK MASTER"
    if mode == "BALLER":
        return f"{season_text} LEGENDARY BALLER"

    if mode == "SNOWDAY":
        if is_gc or mode == "WIZARD":
            return f"{season_text} BLIZZARD WIZARD"
        return f"{season_text} ICE TITAN"
    if mode == "WIZARD":
        return f"{season_text} BLIZZARD WIZARD"
    if mode == "TITAN":
        return f"{season_text} ICE TITAN"

    if is_gc:
        return f"{season_text} GRAND CHAMPION"
    return f"{season_text} SUPERSONIC LEGEND"


class PlayerTitle:
    """PlayerTitle()
    Represents Rocket League player title.

    Attributes
    ----------
    id: str
        Title's ID.
    """

    __slots__ = ("id",)

    def __init__(self, title_id: str) -> None:
        self.id = title_id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} name={self.name!r}>"

    @property
    def name(self) -> str:
        """
        The English name of the title, as shown in the game.

        For tournament winner rewards, the following strings are used where rank images
        should be rendered:

        - ``{{BRONZE}}`` - Bronze
        - ``{{SILVER}}`` - Silver
        - ``{{GOLD}}`` - Gold
        - ``{{PLATINUM}}`` - Platinum
        - ``{{DIAMOND}}`` - Diamond
        - ``{{CHAMPION}}`` - Champion
        - ``{{GRANDCHAMPION}}`` - Grand Champion
        - ``{{SUPERSONICLEGEND}}`` - Supersonic Legend

        .. note::

            This is not provided by the API itself and is generated by the library
            using a bunch of rules and special cases based on the title's ID.
            It may not remain accurate as the time goes by without updating the library.
        """
        id_ = self.id

        # special cases
        special_case_title = _SPECIAL_CASED_TITLE_NAMES.get(id_)
        if special_case_title is not None:
            return special_case_title

        # RLCS n-time World Champion titles
        suffix = "Time_World_Champion"
        if id_.endswith(suffix):
            return f"{id_[:-len(suffix)]}-TIME WORLD CHAMPION"

        id_parts = id_.split("_")
        first = id_parts[0]

        # Per-season tournament winner rewards
        if first == "AutoTour":
            raw_season_number = id_parts[1].lstrip("0")
            rank_name = id_parts[2].upper()
            return f"S{raw_season_number} {{{rank_name}}} TOURNAMENT WINNER"

        # Grand Champion and Supersonic Legend season rewards for all modes
        if _SEASON_REWARD_RE.fullmatch(first):
            return _construct_season_reward_title(id_parts)

        id_parts = [
            part.upper()
            for part in id_parts
            for part in _TITLE_CASE_SPLIT_RE.sub(r" \1", part).strip().split()
        ]
        first = id_parts[0]

        # Grand Champion season rewards
        if first == "SEASON":
            season_number = int(id_parts[1])
            if season_number > 14:
                return f"S{season_number - 14} GRAND CHAMPION"
            return f"SEASON {season_number} GRAND CHAMPION"
        # Kickoff tournament titles
        if first == "KICK":
            return f"THE KICKOFF - {' '.join(id_parts[2:])}"
        # RLCS tournament titles
        if first == "RLCS":
            if id_parts[1].startswith("0"):
                # title id includes season number that needs to be formatted differently
                raw_season_number = id_parts[1].lstrip("0")
                return f"RLCS SEASON {raw_season_number} {' '.join(id_parts[2:])}"
            if (
                len(id_parts) == 4
                and id_parts[1] == "WORLD"
                and id_parts[2] == "CHAMPION"
            ):
                # title id says WORLD CHAMPION CONTENDER/ELITE/FINALIST
                # but it should actually be WORLD CHAMPIONSHIP CONTENDER/ELITE/FINALIST
                return f"RLCS WORLD CHAMPIONSHIP {id_parts[3]}"
            if not (len(id_parts) == 5 and len(id_parts[1]) == len(id_parts[2]) == 2):
                # fallback to standard formatting rules
                pass
            elif id_parts[3] == "WORLD":
                # title id for world champion includes two 2-digit years, i.e. 21_22
                # and they need to be formatted as: 2021-22
                return f"RLCS 20{id_parts[1]}-{id_parts[2]} WORLD CHAMPION"
            elif id_parts[3] == "REGIONAL":
                # title id includes year but the name shouldn't
                return f"RLCS REGIONAL {id_parts[-1]}"
            elif id_parts[3] == "MAJOR":
                # title id includes year but the name should just include "FALL" instead
                return f"RLCS FALL MAJOR {id_parts[-1]}"

        if first == "RLRS":
            raw_season_number = id_parts[1].lstrip("0")
            return f"RIVAL SERIES SEASON {raw_season_number} {' '.join(id_parts[2:])}"
        # special event, XP, fan reward, and Rocket League Sideswipe titles
        if first in ("SE", "XP", "FR", "RLSS"):
            id_parts.pop(0)
        # Rocket Pass titles - second part is its season number
        elif first == "RP":
            id_parts.pop(0)
            id_parts.pop(0)
        # Collegiate Rocket League tournament titles
        elif first == "CRL" and len(id_parts) > 2:
            if id_parts[1].startswith("0"):
                # 2nd part is season number which should not be included in the name
                id_parts.pop(1)
            elif len(id_parts[1]) == 2:
                # 2nd part is 2-digit year
                id_parts[1] = f"20{id_parts[1]}"
            elif len(id_parts[2]) == 2:
                # 3rd part is 2-digit year
                id_parts[2] = f"20{id_parts[2]}"

        return " ".join(id_parts).upper()
