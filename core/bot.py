# core/bot.py
import core.config as config
from core.ocr import OCR
from core.recognizer import Recognizer
from utils.adb_helper import ADB
from utils.log import debug, error, info, warning
from utils.helper import sleep
from utils.assets_repository import get_icon
import utils.constants as CONST

from core.actions.base import Interaction, Input, Navigation
from core.actions import (
    InfirmaryManager,
    SkillManager,
    RaceManager,
    EventManager,
)
from core.flow.flow_manager import FlowManager
from core.state.create_analyzer import create_state_analyzer


class Bot:
    templates = {
        "tazuna": "assets/ui/tazuna_hint.png",
        "unity_cup": "assets/ui/unity_cup_banner.png",
        "retry": "assets/buttons/retry_btn.png",
        "event": "assets/icons/event_choice_1.png",
        "inspiration": "assets/buttons/inspiration_btn2.png",
        "cancel": "assets/buttons/cancel_btn.png",
        "next": "assets/buttons/next_btn.png",
        "next2": "assets/buttons/next2_btn.png",
        "infirmary": "assets/buttons/infirmary_btn.png",
    }

    def __init__(self, adb: ADB = None, scenario: str = None):
        self.is_running = False
        self.adb = adb
        self.scenario = scenario or config.SCENARIO

        CONST.ACTIVE_SCENARIO = self.scenario
        debug(f"Bot scenario: {self.scenario}")
        debug(f"Global CONST: {CONST.ACTIVE_SCENARIO}")

        # Initialize components
        self.ocr = OCR()
        self.recognizer = Recognizer(0.8, adb)
        self.state_analyzer = create_state_analyzer(
            self.scenario, self.ocr, self.recognizer
        )

        self.input = Input(adb, self)
        self.interaction = Interaction(self.input, self.recognizer)
        self.navigation = Navigation(self.interaction)

        self.skill_manager = SkillManager(self.interaction, self.ocr, self.navigation)
        self.infirmary_manager = InfirmaryManager(self.interaction, self.state_analyzer)
        self.event_manager = EventManager(self.interaction, self.ocr)
        self.race_manager = RaceManager(self.interaction, self.navigation, self.ocr)

        self.flow_manager = FlowManager(
            self.adb,
            self.ocr,
            self.recognizer,
            self.state_analyzer,
            self.input,
            self.interaction,
            self.navigation,
            self.skill_manager,
            self.infirmary_manager,
            self.event_manager,
            self.race_manager,
        )

    def start(self):
        self.is_running = True
        self.flow_manager.activate(config.SCENARIO)
        info("Bot starting...")

    def stop(self):
        self.is_running = False
        info("Bot stopped.")

    def run(self):
        while self.is_running:
            sleep(0.5)

            # 1. take screenshot
            screen = self.adb.screenshot()

            # 2. Handle UI elements
            matches = self.recognizer.multi_match_templates(self.templates, screen)

            if self.event_manager.select_event(screen):
                continue
            if self.interaction.click_boxes(
                matches["inspiration"], text="Inspiration found."
            ):
                continue
            if matches["cancel"]:
                if self.recognizer.locate_on_screen(get_icon("clock_icon")):
                    debug("Lost race, wait for input")
                    continue
                else:
                    self.interaction.click_boxes(matches["cancel"], text="cancel.")
                    continue
            if self.interaction.click_boxes(matches["next"], text="next."):
                continue
            if self.interaction.click_boxes(matches["next2"], text="next2."):
                continue
            if self.interaction.click_boxes(matches["retry"], text="retry"):
                continue

            if matches["unity_cup"]:
                self.flow_manager.run(screen, matches)
                continue
            if not matches["tazuna"]:
                print(".", end="")
                continue

            self.flow_manager.run(screen, matches)
