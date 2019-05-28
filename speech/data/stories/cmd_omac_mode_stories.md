## execute cmd omac mode
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
    
## execute cmd omac mode 2 cmd
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
    - utter_anything_else
    
## execute cmd omac mode 3 cmd
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
    - utter_anything_else

## greeting + omac mode cmd
* greet
    - action_greet_user
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
    
## greeting + what is possible + omac mode cmd
* greet
    - action_greet_user   
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
    - utter_anything_else

## what is possible + omac mode cmd
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
    
## omac mode cmd + chichat
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    
## chichat + mode cmd + chichat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    
## mode cmd + chichat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* omac_cmd_mode
    - utter_cmd_executing
    - action_execute_cmd_omac_mode
