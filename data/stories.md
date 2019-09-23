## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
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
* goodbye
  - utter_goodbye

## news_1
* greet
  - utter_greet
* ask_4_news
  - utter_news
* thanks
  - utter_thanks1
  - utter_thanks2

## music
* want_a_song
  - utter_music

## video
* want_a_video
  - utter_video
