# -*- coding: utf-8 -*-
import json
import logging
import random

import requests
from rasa_sdk import Action
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
)

logger = logging.getLogger(__name__)


class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self):
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet":
            if shown_privacy and name_entity and name_entity.lower() != "tobi":
                dispatcher.utter_template("utter_greet_name", tracker, name=name_entity)
                return []
            elif shown_privacy:
                dispatcher.utter_template("utter_greet_noname", tracker)
                return []
            else:
                dispatcher.utter_template("utter_greet", tracker)
                dispatcher.utter_template("utter_inform_privacypolicy", tracker)
                dispatcher.utter_template("utter_ask_whatspossible", tracker)
                # dispatcher.utter_template("utter_ask_whatspossible", tracker)
                return [SlotSet("shown_privacy", True)]
        elif intent[:-1] == "get_started_step" and not shown_privacy:
            dispatcher.utter_template("utter_greet", tracker)
            dispatcher.utter_template("utter_inform_privacypolicy", tracker)
            dispatcher.utter_template("utter_" + intent, tracker)
            return [SlotSet("shown_privacy", True), SlotSet("step", intent[-1])]
        elif intent[:-1] == "get_started_step" and shown_privacy:
            dispatcher.utter_template("utter_" + intent, tracker)
            return [SlotSet("step", intent[-1])]
        return []


class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(
            requests.get(
                "http://slowwly.robertomurray.co.uk/delay/3000/url/https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionExecuteOMACStateCmd(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_cmd_omac_state"

    def run(self, dispatcher, tracker, domain):
        # Parse the command
        state_entity = next(tracker.get_latest_entity_values("state_cmd"), None)
        # execute OMAC STATE CMD
        # Start the execution
        # TODO: Implemets using the Demonstrator API
        request = json.loads(
            requests.get(
                "http://slowwly.robertomurray.co.uk/delay/3000/url/https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        # Set the response depending on the results
        dispatcher.utter_template("utter_cmd_executed_success", tracker)
        return [SlotSet("current_omac_state", "execute")]


class ActionExecuteOMACModeCmd(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_execute_cmd_omac_mode"

    def run(self, dispatcher, tracker, domain):
        # Parse the command
        state_entity = next(tracker.get_latest_entity_values("state_cmd"), None)
        # execute OMAC STATE CMD
        # Start the execution
        # TODO: Implemets using the Demonstrator API
        request = json.loads(
            requests.get(
                "http://slowwly.robertomurray.co.uk/delay/3000/url/https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        # Set the response depending on the results
        dispatcher.utter_template("utter_cmd_executed_success", tracker)
        return [SlotSet("current_omac_mode", "execute")]


class ActionExecuteCmdGoTo(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_execute_cmd_goto"

    def run(self, dispatcher, tracker, domain):
        # Parse the command
        cmd = next(tracker.get_latest_entity_values("goto_cmd"), None)
        param = next(tracker.get_latest_entity_values("number"), None)
        # execute cmd
        # Start the execution
        # TODO: Implemets using the Demonstrator API
        request = json.loads(
            requests.get(
                "http://slowwly.robertomurray.co.uk/delay/3000/url/https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        # Set the response depending on the results
        dispatcher.utter_template("utter_cmd_executed_success", tracker)
        return [SlotSet("last_goto_cmd", cmd), SlotSet("last_goto_cmd_param", param)]


class ActionShowValue(Action):
    def name(self):
        return "action_show_value"

    def run(self, dispatcher, tracker, domain):
        variable_name = next(tracker.get_latest_entity_values("variable_name"), None)
        variable_value = random.random()
        dispatcher.utter_template("utter_variable_value", tracker, variable_name=variable_name,
                                  variable_value=variable_value)
        return []


class ActionSlow(Action):
    def name(self):
        return "action_slow"

    def run(self, dispatcher, tracker, domain):
        current_velocity = float(tracker.get_slot("current_velocity"))
        next_velocity = 0.9 * current_velocity
        if next_velocity <= 5:
            dispatcher.utter_template("utter_reached_minimum_velocity", tracker)
            next_velocity = 5.0
        return [SlotSet("current_velocity", next_velocity)]


class ActionVerySlow(Action):
    def name(self):
        return "action_very_slow"

    def run(self, dispatcher, tracker, domain):
        current_velocity = float(tracker.get_slot("current_velocity"))
        next_velocity = 0.6 * current_velocity
        if next_velocity <= 5:
            dispatcher.utter_template("utter_reached_minimum_velocity", tracker)
            next_velocity = 5.0
        return [SlotSet("current_velocity", next_velocity)]


class ActionVeryVerySlow(Action):
    def name(self):
        return "action_very_very_slow"

    def run(self, dispatcher, tracker, domain):
        current_velocity = float(tracker.get_slot("current_velocity"))
        next_velocity = 0.3 * current_velocity
        if next_velocity <= 5:
            dispatcher.utter_template("utter_reached_minimum_velocity", tracker)
            next_velocity = 5.0
        return [SlotSet("current_velocity", next_velocity)]


class ActionFast(Action):
    def name(self):
        return "action_fast"

    def run(self, dispatcher, tracker, domain):
        current_velocity = float(tracker.get_slot("current_velocity"))
        next_velocity = 1.2 * current_velocity
        if next_velocity >= 100:
            dispatcher.utter_template("utter_reached_maximum_velocity", tracker)
            next_velocity = 100.0
        return [SlotSet("current_velocity", next_velocity)]


class ActionVeryFast(Action):
    def name(self):
        return "action_very_fast"

    def run(self, dispatcher, tracker, domain):
        current_velocity = float(tracker.get_slot("current_velocity"))
        next_velocity = 1.5 * current_velocity
        if next_velocity >= 100:
            dispatcher.utter_template("utter_reached_maximum_velocity", tracker)
            next_velocity = 100.0
        return [SlotSet("current_velocity", next_velocity)]


class ActionVeryVeryFast(Action):
    def name(self):
        return "action_very_very_fast"

    def run(self, dispatcher, tracker, domain):
        current_velocity = float(tracker.get_slot("current_velocity"))
        next_velocity = 2.0 * current_velocity
        if next_velocity >= 100:
            dispatcher.utter_template("utter_reached_maximum_velocity", tracker)
            next_velocity = 100.0
        return [SlotSet("current_velocity", next_velocity)]


class ActionOpenGripper(Action):
    def name(self):
        return "action_open_gripper"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_template("utter_cmd_executed_success", tracker)
        return []


class ActionCloseGripper(Action):
    def name(self):
        return "action_close_gripper"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_template("utter_cmd_executed_success", tracker)
        return []


class ActionTakeGripper(Action):
    def name(self):
        return "action_take_gripper"

    def run(self, dispatcher, tracker, domain):
        gripper_nummber = next(tracker.get_latest_entity_values("number"), None)
        gripper_hooked = bool(tracker.get_slot("gripper_hooked"))

        # execute cmd
        # Start the execution
        # TODO: Implemets using the Demonstrator API
        request = json.loads(
            requests.get(
                "http://slowwly.robertomurray.co.uk/delay/3000/url/https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        # Set the response depending on the results

        dispatcher.utter_template("utter_cmd_executed_success", tracker)
        return [SlotSet("gripper_hooked", True)]


class ActionReleaseGripper(Action):
    def name(self):
        return "action_release_gripper"

    def run(self, dispatcher, tracker, domain):
        gripper_hooked = bool(tracker.get_slot("gripper_hooked"))

        # execute cmd
        # Start the execution
        # TODO: Implemets using the Demonstrator API
        request = json.loads(
            requests.get(
                "http://slowwly.robertomurray.co.uk/delay/3000/url/https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        # Set the response depending on the results

        dispatcher.utter_template("utter_cmd_executed_success", tracker)
        return [SlotSet("gripper_hooked", False)]


class ActionChitchat(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in [
            "ask_builder",
            "ask_howdoing",
            "ask_whatspossible",
            "ask_whatisdemonstrator",
            "ask_isbot",
            "ask_howold",
            "ask_whoisit"
            "ask_languagesbot",
            "ask_wherefrom",
            "ask_whoami",
            "handleinsult",
            "nicetomeeyou",
            "joke",
            "ask_whatismyname",
            "ask_howbuilt",
            "ask_whoisit",
        ]:
            dispatcher.utter_template("utter_" + intent, tracker)
        return []


class ActionPause(Action):
    """Pause the conversation"""

    def name(self):
        return "action_pause"

    def run(self, dispatcher, tracker, domain):
        return [ConversationPaused()]


class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_default", tracker)
        return [UserUtteranceReverted()]


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self):
        return "action_default_ask_affirmation"

    def __init__(self):
        import pandas as pd

        self.intent_mappings = pd.read_csv("data/" "intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    def run(
            self,
            dispatcher,
            tracker,
            domain,
    ):

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if len(intent_ranking) > 1:
            diff_intent_confidence = intent_ranking[0].get(
                "confidence"
            ) - intent_ranking[1].get("confidence")
            if diff_intent_confidence < 0.2:
                intent_ranking = intent_ranking[:2]
            else:
                intent_ranking = intent_ranking[:1]
        first_intent_names = [
            intent.get("name", "")
            for intent in intent_ranking
            if intent.get("name", "") != "out_of_scope"
        ]

        message_title = (
            "Sorry, I'm not sure I've understood " "you correctly. Do you mean..."
        )

        entities = tracker.latest_message.get("entities", [])
        entities = {e["entity"]: e["value"] for e in entities}

        entities_json = json.dumps(entities)

        buttons = []
        for intent in first_intent_names:
            logger.debug(intent)
            logger.debug(entities)
            buttons.append(
                {
                    "title": self.get_button_title(intent, entities),
                    "payload": "/{}{}".format(intent, entities_json),
                }
            )

        buttons.append({"title": "Something else", "payload": "/out_of_scope"})

        dispatcher.utter_button_message(message_title, buttons=buttons)

        return []


class ActionNextStep(Action):
    def name(self):
        return "action_next_step"

    def run(self, dispatcher, tracker, domain):
        step = int(tracker.get_slot("step")) + 1

        if step in [2, 3, 4]:
            dispatcher.utter_template("utter_continue_step{}".format(step), tracker)
        else:
            dispatcher.utter_template("utter_no_more_steps", tracker)

        return []
