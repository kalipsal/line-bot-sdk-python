from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from kenbot import line_bot_api


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_get_profile"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello World!")
        line_bot_api

        return [SlotSet("superman", 'Ken')]
