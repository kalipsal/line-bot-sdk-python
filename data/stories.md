## happy path
* greet
  - utter_greet
  - action_hello_world
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
  - action_hello_world
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
  - action_hello_world
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## interactive_story_1
* greet
  - utter_greet
  - action_hello_world
* goodbye
  - utter_goodbye

## news_1
* greet
  - utter_greet
  - action_hello_world
  - action_greet
* ask_4_news
  - utter_news
* thanks
  - utter_thanks

## music
* want_a_song
  - utter_music

## video
* want_a_video
  - utter_video

## greet + location/price + cuisine + num people    <!-- name of the story - just for debugging -->
* greet
   - action_ask_howcanhelp
* inform{"location": "rome", "price": "cheap"}  <!-- user utterance, in format intent{entities} -->
   - action_on_it
   - action_ask_cuisine
* inform{"cuisine": "spanish"}
   - action_ask_numpeople        <!-- action that the bot should execute -->
* inform{"people": "six"}
   - action_ack_dosearch
