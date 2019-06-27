## execute cmd omac state
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
    
## execute cmd omac state 2 cmd
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
    - utter_anything_else
    
## execute cmd omac state 3 cmd
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
    - utter_anything_else

## greeting + omac state cmd
* greet
    - action_greet_user
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
    
## greeting + what is possible + omac state cmd
* greet
    - action_greet_user   
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
    - utter_anything_else

## what is possible + omac state cmd
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
    
## cmd + chichat
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    
## cmd + chichat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* omac_cmd_state
    - utter_cmd_executing
    - action_cmd_omac_state
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
