## story_show_privacy_policy
* ask_privacy_policy
  - utter_resume_privacy_policy

## ask_privacy_policy
* greet
    - action_greet_user
* ask_privacy_policy
     - utter_resume_privacy_policy

## ask_privacy_policy more
* greet
    - action_greet_user
* ask_privacy_policy
    - utter_resume_privacy_policy
    
## ask_privacy_policy more other
* ask_privacy_policy
    - utter_resume_privacy_policy
* ask_privacy_policy
    - utter_resume_privacy_policy

## ask_privacy_policy more
* greet
    - action_greet_user
* ask_privacy_policy
    - utter_resume_privacy_policy

## greet + ask_privacy_policy and confirm
* greet
    - action_greet_user
* ask_privacy_policy
    - utter_resume_privacy_policy
    - utter_ask_privacy_policy
* affirm
     - utter_react_positive
     - utter_ask_whatspossible
* deny
    - utter_react_negative
    - utter_goodbye

## ask_privacy_policy and confirm
* ask_privacy_policy
    - utter_resume_privacy_policy
    - utter_ask_privacy_policy
* affirm
     - utter_accept_privacy_policy
     - slot{"privacy_policy_accepted": "True"}
     - utter_react_positive
     - utter_ask_whatspossible
* deny
    - utter_react_negative
    - utter_goodbye
