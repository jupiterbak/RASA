## chitchat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt OR ask_whatspossible
    - action_chitchat

## deny ask_whatspossible
* ask_whatspossible
    - action_chitchat
* deny
    - utter_nohelp

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
    -     - 
## ask_whatspossible more + demo + chichat
* greet
    - action_greet_user
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
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
    
## ask_whatspossible more + demo + chichat
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
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
    
## ask_whatspossible more + demo + chichat
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* ask_whatspossible
    - utter_getstarted
    - utter_explain_demonstratorcore
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* affirm
    - utter_explain_nlu
    - utter_explain_core
* deny
    - utter_explain_stack
    - utter_stack_details

## ask_whatspossible more
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* ask_whatspossible
    - action_chitchat

## new to demonstrator + new to chatbots
* greet
    - action_greet_user
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_stack_details
* deny
    - utter_explain_stack
    - utter_stack_details
* affirm OR how_to_get_started
    - utter_explain_nlu
    - utter_explain_core
    - utter_direct_to_step2


## new to demo + not new to chatbots + not migrating
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_stack_details
* deny
    - utter_explain_stack
    - utter_stack_details
* affirm OR how_to_get_started
    - utter_explain_nlu
    - utter_explain_core
    - utter_direct_to_step2


## new to demo + not new to chatbots
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_stack_details
* deny
    - utter_explain_stack
    - utter_stack_details
* affirm OR how_to_get_started
    - utter_explain_stack
    - utter_stack_details
    - utter_direct_to_step2
    
## new to demo + not new to chatbots
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_stack_details
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
* affirm OR how_to_get_started
    - utter_explain_stack
    - utter_stack_details
    - utter_direct_to_step2

## new to demo + not new to chatbots
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_stack_details
* deny
    - utter_explain_stack
    - utter_stack_details
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* affirm OR how_to_get_started
    - utter_explain_stack
    - utter_stack_details
    - utter_direct_to_step2

## new to demo + not new to chatbots
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* affirm
    - utter_explain_stack
    - utter_stack_details
* deny
    - utter_explain_stack
    - utter_stack_details
* affirm OR how_to_get_started
    - utter_explain_stack
    - utter_stack_details
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_direct_to_step2


## new to demo/bots, explain stack and try it out
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_also_explain_nlu
* affirm OR how_to_get_started
    - utter_explain_stack
    - utter_stack_details
    - utter_direct_to_step2

## new to demo/bots, explain core, then nlu and try out stack
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_also_explain_nlu
* how_to_get_started
    - utter_explain_core
    - utter_also_explain_nlu
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_also_explain_nlu
* affirm
    - utter_explain_nlu
    - utter_direct_to_step2

## new to demo/bots, explain core, then nlu and try out stack
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_also_explain_nlu
* how_to_get_started{"product": "core"}
    - utter_explain_core
    - utter_also_explain_nlu
* affirm
    - utter_explain_nlu
    - utter_direct_to_step2
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_direct_to_step2

## new to rasa/bots, explain nlu and try out stack
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_also_explain_nlu
* how_to_get_started
    - utter_explain_nlu
    - utter_also_explain_core
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_also_explain_core
* deny
    - utter_direct_to_step2

## new to demo/bots, explain nlu and try out stack
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_explain_nlu
* how_to_get_started
    - utter_explain_nlu
    - utter_also_explain_core
* deny
    - utter_direct_to_step2
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_also_explain_core
    - utter_direct_to_step2

## new to demo/bots, don't explain and try out stack
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_also_explain_nlu
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_also_explain_nlu
* deny
    - utter_direct_to_step2

## new to demo/bots, don't explain and try out stack
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_also_explain_nlu
* deny
    - utter_direct_to_step2
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_direct_to_step2


## not new to demo + not interested in products
* greet
    - action_greet_user
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* deny
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup

## not new to demo + not interested in products
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_first_bot_with_rasa
* deny
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup

## not new to demo + not interested in products
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* deny
    - utter_explain_demonstratorcore
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_explain_demonstratorcore
* deny
    - utter_thumbsup


## not new to demo + nlu + intent + pipeline recommendation, spacy
* greet
    - action_greet_user
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* deny
    - utter_explain_demonstratorcore
* how_to_get_started
    - utter_ask_for_nlu_specifics
* affirm
    - utter_what_language
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_what_language
* enter_data{"language": "en"}
    - utter_anything_else

## how to get started without privacy policy
* how_to_get_started
    - utter_getstarted
    - utter_first_bot_with_rasa
* ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatisdemonstrator OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR joke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
    - utter_first_bot_with_rasa
* affirm
    - utter_explain_demonstratorcore
* deny
    - utter_explain_stack
    - utter_stack_details
    - utter_also_explain_nlu
* affirm OR how_to_get_started
    - utter_explain_nlu
    - utter_explain_core
    - utter_direct_to_step2