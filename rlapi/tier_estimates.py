import logging
from math import ceil
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .player import Playlist

log = logging.getLogger(__name__)

__all__ = ('TierEstimates',)


class TierEstimates:
    """
    Represents Rocket League playlist's tier estimates.

    Attributes
    ----------
    playlist: `Playlist`
        Playlist object which these estimates are about.
    tier: int
        Estimated tier on this playlist.
    division: int
        Estimated division on this playlist.
    div_down: int, optional
        Estimated amount of points for player to go a division down.
    div_up: int, optional
        Estimated amount of points for player to go a division up.
    tier_down: int, optional
        Estimated amount of points for player to go a tier down.
    tier_up: int, optional
        Estimated amount of points for player to go a tier up.

    """
    __slots__ = (
        'playlist',
        'tier',
        'division',
        'div_down',
        'div_up',
        'tier_down',
        'tier_up'
    )

    def __init__(self, playlist: 'Playlist'):
        self.playlist = playlist
        self.tier: int
        self.division: int
        if playlist.tier == 0:
            self._estimate_current_tier()
        else:
            self.tier = playlist.tier
            self.division = playlist.division
        self.div_down: Optional[int] = self._estimate_div_down()
        self.div_up: Optional[int] = self._estimate_div_up()
        self.tier_down: Optional[int] = self._estimate_tier_down()
        self.tier_up: Optional[int] = self._estimate_tier_up()

    def _estimate_div_down(self):
        playlist = self.playlist
        if self.tier == 1 and self.division == 0 or self.tier == 0:
            return None
        try:
            divisions = playlist.breakdown[self.tier]
            div_down = int(
                ceil(
                    divisions[self.division][0] - playlist.skill
                )
            )
        except KeyError as e:
            log.debug(str(e))
            return None
        if div_down > 0:
            div_down = -1
        return div_down

    def _estimate_div_up(self):
        playlist = self.playlist
        if self.tier == playlist.tier_max or self.tier == 0:
            return None
        try:
            divisions = playlist.breakdown[self.tier]
            if self.tier == self.division == 0:
                value = divisions[1][0]
            else:
                value = divisions[self.division][1]
            div_up = int(
                ceil(
                    value - playlist.skill
                )
            )
        except KeyError as e:
            log.debug(str(e))
            return None
        if div_up < 0:
            div_up = 1
        return div_up

    def _estimate_tier_down(self):
        playlist = self.playlist
        if self.tier in {0, 1}:
            return None
        try:
            divisions = playlist.breakdown[self.tier]
            tier_down = int(
                ceil(
                    divisions[0][0] - playlist.skill
                )
            )
        except KeyError as e:
            log.debug(str(e))
            return None
        if tier_down > 0:
            tier_down = -1
        return tier_down

    def _estimate_tier_up(self):
        playlist = self.playlist
        if self.tier in {0, playlist.tier_max}:
            return None
        try:
            divisions = playlist.breakdown[self.tier]
            tier_up = int(
                ceil(
                    divisions[3][1] - playlist.skill
                )
            )
        except KeyError as e:
            log.debug(str(e))
            return None
        if tier_up < 0:
            tier_up = 1
        return tier_up

    def _estimate_current_tier(self):
        playlist = self.playlist
        if not playlist.breakdown:
            self.tier = playlist.tier
            self.division = playlist.division
            return

        lowest_diff = None
        for tier, divisions in playlist.breakdown.items():
            for division, (begin, end) in divisions.items():
                if begin <= playlist.skill <= end:
                    self.tier = tier
                    self.division = division
                    return
                diff, incr = min(
                    (abs(playlist.skill-begin), -1),
                    (abs(playlist.skill-end), 1)
                )
                try:
                    condition = diff <= lowest_diff
                except TypeError:
                    condition = True
                if condition:
                    lowest_diff = diff
                    lowest_diff_tier = tier
                    lowest_diff_division = division+incr

        if lowest_diff_division == -1:
            self.tier = lowest_diff_tier-1
            self.division = 3
            if self.tier < 1:
                self.tier = 1
                self.division = 0
        elif lowest_diff_division == 4:
            self.tier = lowest_diff_tier+1
            self.division = 0
            if self.tier > playlist.tier_max:
                self.tier = playlist.tier_max
        else:
            self.tier = lowest_diff_tier
            self.division = lowest_diff_division
