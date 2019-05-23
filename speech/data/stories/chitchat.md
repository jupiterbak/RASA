## story_goodbye
* goodbye
 - utter_goodbye

## story_name
* name{"name":"Tobi"}
 - utter_greet

## thanks
* thanks
  - utter_noworries
  - utter_anything_else

## greet
* greet OR enter_data{"name": "akela"}
  - action_greet_user

## neither options
* greet
  - action_greet_user
* deny
  - utter_nohelp

## anything else? - yes
    - utter_anything_else
* affirm
    - utter_what_help

## anything else? - no
    - utter_anything_else
* deny
    - utter_thumbsup

## anything else?
    - utter_anything_else
* enter_data
    - utter_not_sure
    - utter_possibilities

## positive reaction
* react_positive
    - utter_react_positive

## negative reaction
* react_negative
    - utter_react_negative

## chitchat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt OR ask_whatspossible
    - action_chitchat
     
## chitchat + introduction
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt OR ask_whatspossible
    - action_chitchat   
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_explain_nlu
    - utter_explain_core
* deny
    - utter_thumbsup
    - utter_anything_else

## only ask_whatspossible
* ask_whatspossible
    - action_chitchat
    
## ask_whatspossible
* ask_whatspossible
    - action_chitchat
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_explain_nlu
    - utter_explain_core
* deny
    - utter_thumbsup
    - utter_anything_else


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

## greet + ask_whatspossible + help
* greet
    - action_greet_user
* ask_whatspossible    
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_explain_nlu
    - utter_explain_core
    - utter_anything_else
    
## greet + ask_whatspossible + help
* greet
    - action_greet_user
* ask_whatspossible    
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup
    - utter_anything_else

## ask_whatspossible more
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* ask_whatspossible
    - action_chitchat

## ask_whatspossible more demo + affirm
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* affirm
    - utter_explain_nlu
    - utter_explain_core
    
## ask_whatspossible more demo + deny
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* deny
    - utter_thumbsup
    - utter_anything_else
    
## explain more demo + affirm
* greet
    - action_greet_user
* explain
    - utter_whoiam
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_nlu
    - utter_explain_core
    
## explain more demo + deny
* greet
    - action_greet_user
* explain
    - utter_whoiam
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup
    - utter_anything_else

    
## ask_whatspossible more demo + affirm
* greet
    - action_greet_user
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_nlu
    - utter_explain_core
    
## ask_whatspossible more demo + deny
* greet
    - action_greet_user
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup
    - utter_anything_else
    
## source code
* source_code
    - utter_source_code
    - utter_anything_else
    
## is it open sourced    
* ask_if_opensource
    - utter_source_code
    - utter_anything_else
    
## who is it + explain  + affirm  
* ask_whoisit OR ask_howbuilt OR ask_whatspossible
    - action_chitchat
* explain
    - utter_whoiam
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_explain_nlu
    - utter_explain_core
    
## who is it + explain + deny   
* ask_whoisit OR ask_howbuilt OR ask_whatspossible
    - action_chitchat
* explain
    - utter_whoiam
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup
    - utter_anything_else
    
## who is it + explain    
* ask_whoisit
    - utter_whoiam
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_explain_nlu
    - utter_explain_core

## who is it + explain + deny    
* ask_whoisit
    - utter_whoiam
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup
    - utter_anything_else
    
## deny ask_whatspossible
* ask_whatspossible
    - action_chitchat
* deny
    - utter_nohelp
    
## anything else + chichat
    - utter_anything_else
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
 