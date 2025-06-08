from typing import Any, Dict, List, Optional

from .enums import Platform

__all__ = (
    "PopulationPlaylist",
    "KNOWN_POPULATION_PLAYLISTS",
    "PlaylistPopulation",
    "Population",
)


class PopulationPlaylist:
    """PopulationPlaylist()
    Describes a Rocket League playlist that may be returned by population endpoint.

    When `is_known` is ``False``, only the ID will be filled with the right value.

    Attributes
    ----------
    id: int
        Playlist's ID. For ranked playlists, this is consistent with `PlaylistKey`.
    title: str
        Playlist's title.
        When `is_known` is ``False``, this will be set to "Unknown".
    description: str, optional
        Playlist's description, if available.
    player_count: int
        Number of players that the match in this playlist can have in total.

        ``None`` if the value is not fixed.

        ``1`` if the playlist is not a match (e.g. Main Menu, Training, etc.).
    ranked: bool
        Indicates whether the playlist is ranked.
    online: bool
        Indicates whether the playlist is online.
    private: bool
        Indicates whether the match is private or if matchmaking was involved.
    is_ltm: bool
        Indicates whether the playlist is a Limited Time Mode (LTM).
    is_known: bool
        Indicates whether the playlist is known to this library.
        When this is ``False``, all fields except for ``id`` will not have
        the right values.
    """

    __slots__ = (
        "id",
        "title",
        "description",
        "player_count",
        "ranked",
        "online",
        "private",
        "is_ltm",
        "is_known",
    )

    def __init__(
        self,
        id: int,
        title: str,
        *,
        description: Optional[str] = None,
        player_count: Optional[int] = None,
        ranked: bool = False,
        online: bool = True,
        private: Optional[bool] = None,
        is_ltm: bool = False,
        is_known: bool = True,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.player_count = player_count
        self.ranked = ranked
        self.is_ltm = is_ltm
        self.online = online
        if private is None:
            self.private = not online
        else:
            self.private = private
        self.is_known = is_known

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f" {self.title} ({self.id})"
            f" player_count={self.player_count}"
            ">"
        )


_KNOWN_PLAYLISTS = (
    PopulationPlaylist(-2, "Searching for Match", player_count=1, online=False),
    PopulationPlaylist(0, "Main Menu", player_count=1, online=False),
    # Casual online modes
    PopulationPlaylist(1, "Duel", description="One-on-one", player_count=2),
    PopulationPlaylist(2, "Doubles", description="Play with a partner", player_count=4),
    PopulationPlaylist(3, "Standard", description="Classic team play", player_count=6),
    PopulationPlaylist(4, "Chaos", description="Complete mayhem", player_count=8),
    # 5 is unknown
    #
    # Private online match
    PopulationPlaylist(6, "Private Match", private=True),
    # Offline modes
    PopulationPlaylist(7, "Season", online=False),
    PopulationPlaylist(
        # also known as OfflineSplitscreen
        8,
        "Exhibition",
        online=False,
    ),
    PopulationPlaylist(9, "Training", player_count=1, online=False),
    # Competitive online standard modes
    PopulationPlaylist(
        10, "Ranked Duel", description="Ranked one-on-one", player_count=2, ranked=True
    ),
    PopulationPlaylist(
        11,
        "Ranked Doubles",
        description="Ranked play with a partner",
        player_count=2,
        ranked=True,
    ),
    PopulationPlaylist(
        # mode no longer available
        12,
        "Ranked Solo Standard",
        player_count=6,
        ranked=True,
    ),
    PopulationPlaylist(
        13,
        "Ranked Standard",
        description="Ranked play with a team",
        player_count=6,
        ranked=True,
    ),
    # 14 is unknown
    #
    # No longer available casual modes
    PopulationPlaylist(
        15, "Snow Day", description="Play with a hockey puck", player_count=6
    ),
    PopulationPlaylist(
        16,
        "Rocket Labs",
        description="Rocket Labs features experimental Arenas",
        player_count=6,
    ),
    PopulationPlaylist(
        17, "Hoops", description="Play with a basketball", player_count=4
    ),
    PopulationPlaylist(18, "Rumble", description="Play with power-ups", player_count=6),
    # Offline modes
    PopulationPlaylist(19, "Workshop", player_count=1, online=False),
    PopulationPlaylist(20, "Custom Training Editor", player_count=1, online=False),
    PopulationPlaylist(21, "Custom Training", player_count=1, online=False),
    # Online custom tournaments - they may be public or private
    PopulationPlaylist(22, "Custom Tournament"),
    # No longer available casual extra mode
    PopulationPlaylist(
        23, "Dropshot", description="Break the floor and score", player_count=6
    ),
    # Offline mode
    PopulationPlaylist(24, "LAN Match"),
    # Online casual mode for Anniversary event
    PopulationPlaylist(25, "Anniversary", player_count=6),
    # FACEIT online match
    PopulationPlaylist(26, "External Match (FACEIT)", private=True),
    # Competitive online extra modes
    PopulationPlaylist(
        27,
        "Ranked Hoops",
        description="Play with a basketball",
        player_count=4,
        ranked=True,
    ),
    PopulationPlaylist(
        28,
        "Ranked Rumble",
        description="Play with power-ups",
        player_count=6,
        ranked=True,
    ),
    PopulationPlaylist(
        29,
        "Ranked Dropshot",
        description="Break the floor and score",
        player_count=6,
        ranked=True,
    ),
    PopulationPlaylist(
        30,
        "Ranked Snow Day",
        description="Play with a hockey puck",
        player_count=6,
        ranked=True,
    ),
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        31,
        "Ghost Hunt",
        description=(
            "Use your car's Proton Pack to ensnare the ball and carry it to"
            " the opposing team's Containment Zone. A point is scored"
            " if the ball remains in the Containment Zone for two seconds."
            " Score more than the opposing team before time runs out."
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        32,
        "Beach Ball",
        description=(
            "The ball is lighter and curves just like a beach ball in this 2v2 mode."
            " Enjoy the sun of Salty Shores and have fun!"
        ),
        player_count=4,
        is_ltm=True,
    ),
    PopulationPlaylist(
        33,
        "Spike Rush",
        description=(
            "All players have Spikes which automatically engage after kickoff,"
            " allowing them to stick the ball to their car by driving into it."
            " The ball carrier cannot use or collect boost, is easily demolished by"
            " opposing players, and can manually disengage their car's spikes to"
            " release the ball. Score by getting the ball into your opponent’s goal"
            " by any means."
        ),
        player_count=6,
        is_ltm=True,
    ),
    # Official ranked tournaments organized regularly
    PopulationPlaylist(34, "Official Tournament", ranked=True),
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        35,
        "Rocket Labs",
        description="Rocket Labs features experimental Arenas",
        player_count=6,
        is_ltm=True,
    ),
    # 36 is unknown though it might be sth called "Rumble Labs"?
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        37,
        "Dropshot Rumble",
        description=(
            "Dropshot and Rumble have collided! Get ready to break your opponents'"
            " floor, but now with the power-ups of Rumble!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        38,
        "Heatseeker",
        description=(
            "Touching the ball automatically sends it in the direction of"
            " the opposing team's goal in this speedy game of 3v3."
            " It fires back toward your goal if it hits the backboard, so be careful!"
            " The ball gains speed with each touch. Scoring 7 goals wins!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    # 39 is unknown though it might be something called "Inverted Ball"?
    # 40 is unknown
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        41,
        "Boomer Ball",
        description=(
            "Feel the boom in this twist on classic 3v3 Soccar!"
            " Ball speed and bounciness are increased. Boost is more powerful"
            " and unlimited. Touch the ball and watch it ricochet around the arena!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    # 42 is unknown
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        43,
        "Heatseeker Doubles",
        description=(
            "Heatseeker is now 2v2!"
            " Touching the ball automatically sends it in"
            " the direction of the opposing team’s goal. It fires back toward your goal"
            " if it hits the backboard, so be careful!"
            " The ball gains speed with each touch. Scoring 7 goals wins!"
        ),
        player_count=4,
        is_ltm=True,
    ),
    PopulationPlaylist(
        44,
        "Winter Breakaway",
        description=(
            "Drop the puck and face off on snowy Throwback Stadium!"
            " Just like Snow Day, the ball has been replaced with"
            " a hockey puck in this 3v3 limited time mode."
        ),
        player_count=6,
        is_ltm=True,
    ),
    # 45 is unknown though it might be something called "Rocket Labs Doubles"?
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        46,
        "Gridiron",
        description=(
            "Huddle up and learn the rules of Gridiron:\n"
            "- The standard Rocket League ball has been replaced with"
            " an American football in this 4v4 mode.\n"
            "- Touching the ball attaches it to the roof of your car."
            " Handoff to a teammate or pass it downfield by dodging."
            " Double jumping drops the ball.\n"
            "- Goals scored while the ball is attached are worth 7 points."
            " Goals that are passed in or loose balls that score are worth 3 points."
            " All own-goals are also worth 3 points.\n"
            "- Stay in bounds! You'll fumble the ball if you cross the line marked on"
            " the Arena wall.\n"
            " Now hit the Gridiron and have fun!"
        ),
        player_count=8,
        is_ltm=True,
    ),
    PopulationPlaylist(
        47,
        "Super Cube",
        description=(
            "Square up for 3v3 Super Cube! The ball has been replaced with"
            " a Cube with increased maximum speed and bounciness. Think fast!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        48,
        "Tactical Rumble",
        description=(
            "Rumble has evolved! Instead of getting one random power-up, players will"
            " receive three to choose from. When one is used, three new power-ups will"
            " appear following a cooldown. Some power-ups have a longer cooldown than"
            " others, so choose wisely!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        49,
        "Spring Loaded",
        description=(
            "Spring into this 3v3 Rumble variant where power-ups"
            " have been replaced by the Haymaker and Boot."
            " Boot your opponents and punch your ticket to victory!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        50,
        "Speed Demon",
        description=(
            "Put the pedal to the metal in this 3v3, lightning-quick variant of"
            " Boomer Ball. Boost is unlimited and double the power. The ball is"
            " larger and moves at super fast speed, but with less bounciness."
            " Demolitions occur on contact, but a 1-second respawn timer gets you"
            " right back into the action."
        ),
        player_count=6,
        is_ltm=True,
    ),
    # 51 is unknown
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        52,
        "Gotham City Rumble",
        description=(
            "Gotham City's Super-Villains have taken over Rumble! All power-ups in"
            " Gotham City Rumble are themed after Batman and his Rogues Gallery."
            " Hit Beckwith Park (Gotham Night) in this epic showdown between"
            " good and evil!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    # 53 is unknown
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        54,
        "Knockout",
        description=(
            "In this destructive derby, only the strong survive."
            " 3 lives each, and the last car standing wins!\n\n"
            "- Attack: Dodge into your opponents to send them flying.\n\n"
            "- Block: Backward dodge to reflect damage back at attacking players.\n\n"
            "- Grab: Hold left trigger while dodging to Grab an opponent."
            " Dodge again to throw."
        ),
        player_count=8,
        is_ltm=True,
    ),
    PopulationPlaylist(
        55,
        "confidential_thirdwheel_test",
        description=(
            "Devin will fill this in later."
            " Try to make 3 wheels sound like a good thing."
        ),
        player_count=6,
        is_ltm=True,
    ),
    # 56-61 are unknown
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        62,
        "Nike FC Showdown",
        description=(
            "Football meets Soccar in a Nike-Branded Arena! Nike FC Showdown uses a new"
            " Nike Ball that curves through the air with modified Mutator Settings."
            " Higher max speed and low bounce mean that this LTM is best played"
            " fast and close to the ground."
        ),
        player_count=8,
        is_ltm=True,
    ),
    # 63 is unknown
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        64,
        "Haunted Heatseeker (2v2)",
        description=(
            "Heatseeker is now 2v2!"
            " Touching the ball automatically sends it in"
            " the direction of the opposing team’s goal. It fires back toward your goal"
            " if it hits the backboard, so be careful!"
            " The ball gains speed with each touch. Scoring 7 goals wins!"
        ),
        player_count=4,
        is_ltm=True,
    ),
    PopulationPlaylist(
        65,
        "Haunted Heatseeker (3v3)",
        description=(
            "The spooky side of Heatseeker!"
            " Touching the ball automatically sends it in"
            " the direction of the opposing team’s goal. It fires back toward your goal"
            " if it hits the backboard, so be careful!"
            " The ball gains speed with each touch. Scoring 7 goals wins!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        66,
        "Heatseeker Ricochet",
        description=(
            "Heatseeker with a fun twist thanks to three unique Rocket Labs Arenas:"
            " Barricade, Colossus, and Hourglass."
            " Touching the ball automatically sends it in"
            " the direction of the opposing team's goal."
            " The ball gains speed with each touch. Scoring 7 goals wins!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        67,
        "Spooky Cube",
        description=(
            "Ready to smash some pumpkins? Spooky Cube will put your reflexes to"
            " the test as this jack-o'-lantern cube ricochets around Farmstead (Spooky)"
            " Arena. With a mess of mutators increasing max speed and bounciness,"
            " you’ll need a lot of luck chasing this pumpkin down!"
        ),
        player_count=6,
        is_ltm=True,
    ),
    PopulationPlaylist(
        68,
        "G-Force Frenzy",
        description=(
            "In this new Limited Time Mode you will battle 3x3 in low gravity,"
            " plus use an added unlimited boost, 5x its usual power, to send you"
            " hurtling through the air. Reckon you’re up to the task, pilot?"
        ),
        player_count=6,
        is_ltm=True,
    ),
    # 69 is unknown
    #
    # Limited Time Modes (LTMs)
    PopulationPlaylist(
        70,
        "Dropshot Rumble (2v2)",
        description=(
            "Dropshot and Rumble have collided! Get ready to break your opponents'"
            " floor, but now with the power-ups of Rumble!"
        ),
        player_count=4,
        is_ltm=True,
    ),
)
#: A mapping of known population playlist IDs to their `PopulationPlaylist` objects.
KNOWN_POPULATION_PLAYLISTS = {playlist.id: playlist for playlist in _KNOWN_PLAYLISTS}


class PlaylistPopulation:
    """PlaylistPopulation()
    Describes population of a Rocket League playlist.

    Attributes
    ----------
    playlist: `PopulationPlaylist`
        Playlist that this instance refers to.
        If the playlist is known, this will use a constant value
        with additional information.
    platforms: dict
        Mapping of platforms (`Platform`) to their number of online players (`int`)
        for this playlist.
    """

    __slots__ = ("playlist", "platforms")

    def __init__(self, playlist_id: int) -> None:
        try:
            self.playlist = KNOWN_POPULATION_PLAYLISTS[playlist_id]
        except KeyError:
            self.playlist = PopulationPlaylist(playlist_id, "Unknown", is_known=False)
        self.platforms: Dict[Platform, int] = {}

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f" playlist={self.playlist!r}"
            f" num_players={self.num_players}"
            ">"
        )

    @property
    def num_players(self) -> int:
        """
        Total number of players who are currently online on this playlist
        across all platforms.
        """
        return sum(num_players for num_players in self.platforms.values())


class Population:
    """Population()
    Describes Rocket League's population across all platforms.

    Attributes
    ----------
    playlists: dict
        Mapping of playlist IDs (`int`) to their population (`PlaylistPopulation`).
        For ranked playlists, it is possible to do a lookup by their `PlaylistKey`.
    """

    __slots__ = ("playlists",)

    def __init__(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self.playlists: Dict[int, PlaylistPopulation] = {}
        for raw_platform, raw_population in data.items():
            platform = Platform(raw_platform)
            for raw_population_entry in raw_population:
                playlist_id = raw_population_entry["PlaylistID"]
                playlist_population = self.playlists.get(playlist_id)
                if playlist_population is None:
                    playlist_population = PlaylistPopulation(playlist_id)
                    self.playlists[playlist_id] = playlist_population

                num_players = raw_population_entry["NumPlayers"]
                playlist_population.platforms[platform] = num_players

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} num_players={self.num_players}>"

    @property
    def num_players(self) -> int:
        """
        Total number of players who are currently online on all platforms and playlists.
        """
        return sum(population.num_players for population in self.playlists.values())
