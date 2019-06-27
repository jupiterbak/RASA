## execute cmd goto
* cmd_goto{"goto_cmd":"gripper","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"gripper"}
    - slot{"last_goto_cmd_param":"1"}
    
## execute cmd goto 2 cmd
* cmd_goto{"goto_cmd":"gripper","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"gripper"}
    - slot{"last_goto_cmd_param":"1"}
* cmd_goto{"goto_cmd":"gripper","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"gripper"}
    - slot{"last_goto_cmd_param":"1"}
    - utter_anything_else
    
## execute cmd goto 3 cmd
* cmd_goto{"goto_cmd":"position","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"position"}
    - slot{"last_goto_cmd_param":"1"}
* cmd_goto{"goto_cmd":"gripper","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"gripper"}
    - slot{"last_goto_cmd_param":"1"}
* cmd_goto{"goto_cmd":"position","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"position"}
    - slot{"last_goto_cmd_param":"1"}
    - utter_anything_else

## greeting + goto cmd
* greet
    - action_greet_user
* cmd_goto{"goto_cmd":"gripper","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"gripper"}
    - slot{"last_goto_cmd_param":"1"}
    
## greeting + what is possible + goto cmd
* greet
    - action_greet_user   
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* cmd_goto{"goto_cmd":"gripper","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"gripper"}
    - slot{"last_goto_cmd_param":"1"}
    - utter_anything_else

## what is possible + goto cmd
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* cmd_goto{"goto_cmd":"gripper","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"gripper"}
    - slot{"last_goto_cmd_param":"1"}
    
## cmd + chichat
* cmd_goto{"goto_cmd":"position","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"position"}
    - slot{"last_goto_cmd_param":"1"}
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    
## cmd + chichat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* cmd_goto{"goto_cmd":"position","number":"1"}
    - utter_cmd_executing
    - action_execute_cmd_goto
    - slot{"last_goto_cmd":"position"}
    - slot{"last_goto_cmd_param":"1"}
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
