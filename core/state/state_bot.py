# core/state/state_bot.py
from dataclasses import dataclass
from typing import Dict, Union, Any

import utils.constants as constants
import core.config as config


@dataclass
class BotState:
    mood: str
    turn: Union[int, str]
    year: str
    energy_level: float
    max_energy: float
    current_stats: Dict[str, int]
    criteria: str
    skill_pts: int
    extra: Dict[str, Any] = None

    @property
    def missing_energy(self) -> float:
        """Calculate how much energy is missing"""
        return self.max_energy - self.energy_level

    @property
    def is_race_day(self) -> bool:
        return self.turn == "Race Day" or self.turn == "GOAL"

    @property
    def is_junior_year(self) -> bool:
        return "Junior" in self.year

    @property
    def is_pre_debut(self) -> bool:
        return "Pre" in self.year or "Debut" in self.year

    @property
    def is_summer(self) -> bool:
        return not self.is_junior_year and ("Jul" in self.year or "Aug" in self.year)

    @property
    def is_buy_skill(self) -> bool:
        if config.IS_AUTO_BUY_SKILL:
            return self.skill_pts > config.SKILL_PTS_CHECK

    @property
    def should_visit_infirmary(self) -> bool:
        """Check if should visit infirmary based on energy"""
        return self.missing_energy >= config.SKIP_INFIRMARY_UNLESS_MISSING_ENERGY

    @property
    def needs_increase_mood(self) -> bool:
        mood_index = constants.MOOD_LIST.index(self.mood)
        min_mood = constants.MOOD_LIST.index(
            config.MINIMUM_MOOD_JUNIOR_YEAR
            if self.is_junior_year
            else config.MINIMUM_MOOD
        )
        return mood_index < min_mood

    @property
    def never_rest(self) -> bool:
        return (
            config.NEVER_REST_ENERGY > 0
            and self.energy_level > config.NEVER_REST_ENERGY
        )

    @property
    def should_prioritize_g1(self) -> bool:
        """Should prioritize G1 races based on config and current state"""
        return (
            config.PRIORITIZE_G1_RACE and not self.is_summer and not self.is_pre_debut
        )

    @property
    def should_race_for_goals(self) -> bool:
        """Should race for fan/maiden goals"""
        return (
            not self.is_pre_debut
            and self.turn < 10
            and ("fan" in self.criteria or "Maiden" in self.criteria)
        )
