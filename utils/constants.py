MOOD_LIST = ["AWFUL", "BAD", "NORMAL", "GOOD", "GREAT", "UNKNOWN"]
# Severity -> 0 is doesn't matter / incurable, 1 is "can be ignored for a few turns", 2 is "must be cured immediately"
BAD_STATUS_EFFECTS = {
    "Migraine": {
        "Severity": 2,
        "Effect": "Mood cannot be increased",
    },
    "Night Owl": {
        "Severity": 1,
        "Effect": "Character may lose energy, and possibly mood",
    },
    "Practice Poor": {
        "Severity": 1,
        "Effect": "Increases chance of training failure by 2%",
    },
    "Skin Outbreak": {
        "Severity": 1,
        "Effect": "Character's mood may decrease by one stage.",
    },
    "Slacker": {
        "Severity": 2,
        "Effect": "Character may not show up for training.",
    },
    "Slow Metabolism": {
        "Severity": 2,
        "Effect": "Character cannot gain Speed from speed training.",
    },
    "Under the Weather": {
        "Severity": 0,
        "Effect": "Increases chance of training failure by 5%",
    },
}

GOOD_STATUS_EFFECTS = {
    "Charming": "Raises Friendship Bond gain by 2",
    "Fast Learner": "Reduces the cost of skills by 10%",
    "Hot Topic": "Raises Friendship Bond gain for NPCs by 2",
    "Practice Perfect": "Lowers chance of training failure by 2%",
    "Shining Brightly": "Lowers chance of training failure by 5%",
}

SCENARIO_URA = {
    # X, Y, W, H
    "MOOD_REGION": (555, 125, 130, 25),
    "TURN_REGION": (110, 82, 100, 51),
    "FAILURE_REGION": (145, 790, 505, 20),
    "YEAR_REGION": (105, 35, 165, 20),
    "CRITERIA_REGION": (305, 85, 245, 30),
    "SKILL_PTS_REGION": (610, 780, 65, 35),
    "EVENT_NAME_REGION": (91, 205, 365, 30),
    "SPD_STAT_REGION": (160, 723, 52, 20),
    "STA_STAT_REGION": (255, 723, 52, 20),
    "PWR_STAT_REGION": (350, 723, 52, 20),
    "GUTS_STAT_REGION": (445, 723, 52, 20),
    "WIT_STAT_REGION": (540, 723, 52, 20),
    "TRAINING_ICON_COORD": {
        "spd": (180, 940),
        "sta": (290, 940),
        "pwr": (400, 940),
        "guts": (510, 940),
        "wit": (620, 940),
    },
    # LEFT TOP RIGHT BOTTOM
    "FULL_STATS_STATUS_REGION": (115, 575, 680, 940),
    "RACE_INFO_TEXT_REGION": (135, 335, 525, 370),
    "SCROLLING_SELECTION_MOUSE_POS": (410, 680),
    "SKILL_SCROLL_BOTTOM_MOUSE_POS": (410, 850),
    "RACE_SCROLL_BOTTOM_MOUSE_POS": (410, 860),
    "SUPPORT_CARD_ICON_BBOX": (695, 155, 795, 700),
    "ENERGY_BBOX": (290, 120, 650, 160),
    "RACE_BUTTON_IN_RACE_BBOX_LANDSCAPE": (650, 950, 1000, 1050),
}

SCENARIO_UNITY = {
    # X, Y, W, H
    "MOOD_REGION": (555, 125, 130, 25),
    "TURN_REGION": (110, 60, 63, 43),
    "UNITY_TURN_REGION": (125, 111, 35, 22),
    "FAILURE_REGION": (145, 790, 505, 20),
    "YEAR_REGION": (240, 35, 175, 20),
    "CRITERIA_REGION": (305, 85, 245, 30),
    "SKILL_PTS_REGION": (610, 780, 65, 35),
    "EVENT_NAME_REGION": (91, 205, 365, 30),
    "SPD_STAT_REGION": (160, 723, 52, 20),
    "STA_STAT_REGION": (255, 723, 52, 20),
    "PWR_STAT_REGION": (350, 723, 52, 20),
    "GUTS_STAT_REGION": (445, 723, 52, 20),
    "WIT_STAT_REGION": (540, 723, 52, 20),
    "TRAINING_ICON_COORD": {
        "spd": (180, 940),
        "sta": (290, 940),
        "pwr": (400, 940),
        "guts": (510, 940),
        "wit": (620, 940),
    },
    # LEFT TOP RIGHT BOTTOM
    "FULL_STATS_STATUS_REGION": (115, 575, 680, 940),
    "RACE_INFO_TEXT_REGION": (135, 335, 525, 370),
    "SCROLLING_SELECTION_MOUSE_POS": (410, 680),
    "SKILL_SCROLL_BOTTOM_MOUSE_POS": (410, 850),
    "RACE_SCROLL_BOTTOM_MOUSE_POS": (410, 860),
    "SUPPORT_CARD_ICON_BBOX": (695, 155, 795, 700),
    "ENERGY_BBOX": (290, 120, 650, 160),
    "RACE_BUTTON_IN_RACE_BBOX_LANDSCAPE": (650, 950, 1000, 1050),
}

ACTIVE_SCENARIO = "ura"


class ScenarioConstants:
    def __getattr__(self, key):
        if ACTIVE_SCENARIO == "ura":
            table = SCENARIO_URA
        elif ACTIVE_SCENARIO == "unity":
            table = SCENARIO_UNITY
        else:
            raise KeyError(f"Unknown scenario: {ACTIVE_SCENARIO}")

        try:
            return table[key]
        except KeyError:
            raise AttributeError(
                f"No constant named {key} for scenario {ACTIVE_SCENARIO}"
            )


CONST = ScenarioConstants()
