## execute slow cmd
* slow
    - action_slow
    - slot{"current_velocity": 45.0}
 
## execute very slow cmd
* very_slow
    - action_very_slow
    - slot{"current_velocity": 45.0}

## execute very very slow cmd
* very_very_slow
    - action_very_very_slow
    - slot{"current_velocity": 45.0}

## execute slow cmd x2
* slow
    - action_slow
* slow
    - action_slow
    - utter_anything_else
 
## execute very slow cmd x2
* very_slow
    - action_very_slow
 * very_slow
    - action_very_slow
    - utter_anything_else

## execute very very slow cmd x2
* very_very_slow
    - action_very_very_slow
* very_very_slow
    - action_very_very_slow
    - utter_anything_else

## execute fast cmd
* fast
    - action_fast
    - slot{"current_velocity": 45.0}
 
## execute very fast cmd
* very_fast
    - action_very_fast
    - slot{"current_velocity": 45.0}

## execute very very fast cmd
* very_very_fast
    - action_very_very_fast
    - slot{"current_velocity": 45.0}

## execute fast cmd x2
* fast
    - action_fast
* fast
    - action_fast
    - utter_anything_else
 
## execute very fast cmd x2
* very_fast
    - action_very_fast
 * very_fast
    - action_very_fast
    - utter_anything_else

## execute very very fast cmd x2
* very_very_fast
    - action_very_very_fast
* very_very_fast
    - action_very_very_fast
    - utter_anything_else