# core/flow/scenario/unity.py
from core.flow.base_flow import BaseFlow
from utils.log import info, debug
from utils.assets_repository import get_button
from utils.helper import sleep, get_secs


class UnityFlow(BaseFlow):
    def __init__(self, **deps):
        super().__init__(**deps)

    def run(self, screen, matches):
        unity_cup = matches.get("unity_cup", None)
        if unity_cup:
            self._handle_unity_cup()
            return

        # 3. analyze state
        state = self.state_analyzer.analyze_current_state(screen)

        info("Checking state")

        # 4. Print state info
        print(
            "\n=======================================================================================\n"
        )
        info(f"Year: {state.year}")
        info(f"Mood: {state.mood}")
        info(f"Turn: {state.turn}")
        info(f"Unity Turn: {state.extra["unity_turn"]}")
        info(f"Energy: {state.energy_level:.2f}")
        info(f"Criteria: {state.criteria}")
        if state.is_race_day:
            info(f"Skill pts: {state.skill_pts}")
        else:
            info(f"Stat: {state.current_stats}")
        print(
            "\n=======================================================================================\n"
        )

        # 5. Main game logic
        if state.is_race_day:
            if "Finale" in state.year:
                debug("URA Finale!!!!")
                self.handle_ura_finale(state)
                return
            else:
                debug("Race Day!!!!")
                self.handle_race_day(state)
                return

        if state.should_prioritize_g1:
            debug("Race schedule!")
            if self.handle_g1_race(state):
                return

        if state.should_race_for_goals:
            debug("Race Goal!!")
            if self.handle_goal_race():
                return

        if self.infirmary_manager.handle_infirmary_decision(state, matches, screen):
            debug("Infirmary!")
            return
        if state.needs_increase_mood:
            if self.infirmary_manager.should_force_infirmary_after_skip():
                info(
                    "Severe condition found, visiting infirmary even though we will waste some energy."
                )
                self.infirmary_manager.visit_infirmary()
                return
            info("Mood is low, trying recreation to increase mood")
            self.navigation.do_recreation(state.is_summer)
            return

        debug("handle_training")
        self.handle_training(state)

    def _handle_unity_cup(self):
        info("Handle Unity Cup")
        self.interaction.click_element(get_button("unity_cup_btn"))
        sleep(1)
        select_opponent = self.recognizer.locate_on_screen(
            get_button("select_opponent_btn")
        )
        if select_opponent:
            self.interaction.click_coordinates(300, 480)  # second
            sleep(0.3)
            self.interaction.click_boxes(select_opponent, text="Select opponent")
            sleep(0.5)
            self.interaction.click_element(get_button("begin_showdown_btn"))

        sleep(5)
        self.interaction.click_element(
            get_button("see_all_results_btn"), max_search_time=get_secs(5)
        )
        sleep(2)
        self.interaction.click_element(
            get_button("skip_btn"), clicks=3, max_search_time=get_secs(3)
        )
        sleep(1)
        self.interaction.click_element(get_button("next_btn"))
        sleep(1.5)
        self.interaction.click_element(get_button("next2_btn"))
