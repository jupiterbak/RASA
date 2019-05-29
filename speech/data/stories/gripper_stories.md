## execute cmd open gripper
* cmd_open_gripper
    - utter_cmd_executing
    - action_open_gripper
 
## execute cmd close gripper
* cmd_close_gripper
    - utter_cmd_executing
    - action_close_gripper
    
## execute cmd take gripper
* cmd_take_gripper{"number":1}
    - utter_cmd_executing
    - action_take_gripper
 
## execute cmd release gripper
* cmd_release_gripper
    - utter_cmd_executing
    - action_release_gripper

## execute cmd open gripper x2
* cmd_open_gripper
    - utter_cmd_executing
    - action_open_gripper
* cmd_open_gripper
    - utter_cmd_executing
    - action_open_gripper
    - utter_anything_else
 
## execute cmd close gripper x2
* cmd_close_gripper
    - utter_cmd_executing
    - action_close_gripper
* cmd_close_gripper
    - utter_cmd_executing
    - action_close_gripper
    - utter_anything_else
    
## execute cmd take gripper x2
* cmd_take_gripper
    - utter_cmd_executing
    - action_take_gripper
* cmd_take_gripper
    - utter_cmd_executing
    - action_take_gripper
    - utter_anything_else
 
## execute cmd release gripper x2
* cmd_release_gripper
    - utter_cmd_executing
    - action_release_gripper
* cmd_release_gripper
    - utter_cmd_executing
    - action_release_gripper
    - utter_anything_else