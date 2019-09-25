import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello World!")
        print("=========")
        print(tracker.get_slot('user_id'))
        print("=========")
        print(tracker.current_state())
        print(json.dumps(tracker.current_state(), indent=4, sort_keys=True))

        return [SlotSet("superman", 'Ken')]
