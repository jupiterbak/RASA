## story_goodbye
* goodbye
 - utter_goodbye
 
## story_name
* name{"name":"Tobi"}
 - utter_greet
 
## story_thanks
* thanks
 - utter_awesome

## chitchat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt OR ask_whatspossible
    - action_chitchat

## deny ask_whatspossible
* ask_whatspossible
    - action_chitchat
* deny
    - utter_nohelp
    
## only chitchat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    
## only chitchat more
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat

## more chitchat
* greet
    - action_greet_user
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat

## ask_whatspossible
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat

## ask_whatspossible more
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* ask_whatspossible
    - action_chitchat
    
## ask_whatspossible more + demo
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_nlu
    - utter_explain_core
* deny
    - utter_explain_stack
    - utter_stack_details

