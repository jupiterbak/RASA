# -*- coding: utf-8 -*-
import logging
import requests
from datetime import datetime
from typing import Text, Dict, Any, List
import json

from rasa_core_sdk import Action, Tracker, ActionExecutionRejection
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    FollowupAction,
    Form,
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
            requests.get("https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


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
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_default", tracker)
        return [UserUtteranceReverted()]

class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv("data/" "intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:

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

