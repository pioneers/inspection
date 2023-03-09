import threading
import time
import simpleaudio as sa
from ydl import YDLClient
from alliance import Alliance
from utils import *
from runtimeclient import RuntimeClientManager
from protos.gamestate_pb2 import State
from sheet import Sheet
from robot import Robot


###########################################
# Evergreen Variables
YC = YDLClient(YDL_TARGETS.SHEPHERD)
MATCH_NUMBER: int = -1
GAME_STATE: str = STATE.END

ALLIANCES = {
    ALLIANCE_COLOR.GOLD: Alliance(Robot("", -1), Robot("", -1)),
    ALLIANCE_COLOR.BLUE: Alliance(Robot("", -1), Robot("", -1)),
}

CLIENTS = RuntimeClientManager(YC)

def start():
    '''
    Main loop which processes the event queue and calls the appropriate function
    based on game state and the dictionary of available functions
    '''
    while True:
        payload = YC.receive()
        print("GAME STATE OUTSIDE: ", GAME_STATE)
        print(payload)

        if GAME_STATE in FUNCTION_MAPPINGS:
            func_list = FUNCTION_MAPPINGS.get(GAME_STATE)
            func = func_list.get(payload[1]) or EVERYWHERE_FUNCTIONS.get(payload[1])
            if func is not None:
                func(**payload[2]) #deconstructs dictionary into arguments
            else:
                print(f"Invalid Event in {GAME_STATE}")
        else:
            print(f"Invalid State: {GAME_STATE}")


#we don't need this but its an example of how to pull from the google sheets
def pull_from_sheets():
    while True:
        if not TIMERS.is_paused() and GAME_STATE not in [STATE.END, STATE.SETUP]:
            Sheet.send_scores_for_icons(MATCH_NUMBER) #need this for the future
        time.sleep(2.0)


#NEED
def set_match_number(match_num):
    '''
    Retrieves all match info based on match number and sends this information to the UI.
    If not already cached, fetches info from the spreadsheet, and caches it.
    Fetching info from spreadsheet is asynchronous, will send a ydl header back with results
    '''
    global MATCH_NUMBER
    # if MATCH_NUMBER != match_num:
    #     MATCH_NUMBER = match_num
    #     Sheet.get_match(match_num)
    # else:
    #     send_match_info_to_ui()
    MATCH_NUMBER = match_num
    Sheet.get_match(match_num)


#NEED
def set_teams_info(teams):
    '''
    Caches info and sends it to any open UIs.
    '''
    ALLIANCES[ALLIANCE_COLOR.BLUE].robot1.set_from_dict(teams[INDICES.BLUE_1])
    ALLIANCES[ALLIANCE_COLOR.BLUE].robot2.set_from_dict(teams[INDICES.BLUE_2])
    ALLIANCES[ALLIANCE_COLOR.GOLD].robot1.set_from_dict(teams[INDICES.GOLD_1])
    ALLIANCES[ALLIANCE_COLOR.GOLD].robot2.set_from_dict(teams[INDICES.GOLD_2])
    for i in range(4):
        CLIENTS.connect_client(i, teams[i]["robot_ip"])
    # even if source of info is UI, needs to be forwarded to other open UIs
    send_match_info_to_ui()



###########################################
# Transition Methods
###########################################


def to_setup(match_num, teams):
    '''
    loads the match information for the upcoming match, then
    calls reset_match() to move to setup state.
    By the end, should be ready to start match.
    '''
    if Sheet.write_match_info(match_num, teams) == False:
        return
    global MATCH_NUMBER
    MATCH_NUMBER = match_num
    set_teams_info(teams)
    # note that reset_match is what actually moves Shepherd into the setup state
    reset_match()


#Example of how to send scores to the spreadsheet
def to_end():
    '''
    Go to the end state, finishing the game and flushing scores to the spreadsheet.
    '''
    global GAME_STATE
    GAME_STATE = STATE.END
    disable_robots()
    play_sound("static/trim.wav")
    for n in [0,1,2,3]:
        YC.send(SENSOR_HEADER.TURN_OFF_BUTTON_LIGHT(id=n))
    CLIENTS.close_all()
    GAME_TIMER.reset()
    send_state_to_ui()
    send_score_to_ui()
    flush_scores()

    # temporary code for scrimmage, comment later
    Sheet.write_scores_from_read_scores(MATCH_NUMBER)

    print("ENTERING END STATE")


#maybe
def send_match_info_to_ui():
    '''
    Sends all match info to the UI
    '''
    YC.send(UI_HEADER.TEAMS_INFO(match_num=MATCH_NUMBER, teams=[
        ALLIANCES[ALLIANCE_COLOR.BLUE].robot1.info_dict(CLIENTS.clients[INDICES.BLUE_1].robot_ip),
        ALLIANCES[ALLIANCE_COLOR.BLUE].robot2.info_dict(CLIENTS.clients[INDICES.BLUE_2].robot_ip),
        ALLIANCES[ALLIANCE_COLOR.GOLD].robot1.info_dict(CLIENTS.clients[INDICES.GOLD_1].robot_ip),
        ALLIANCES[ALLIANCE_COLOR.GOLD].robot2.info_dict(CLIENTS.clients[INDICES.GOLD_2].robot_ip),
    ]))

#example of senfing infor to UI 
def send_state_to_ui():
    '''
    Sends the GAME_STATE to the UI
    '''
    end_time, _ = GAME_TIMER.status()
    if GAME_STATE in STAGE_TIMES and end_time is not None:
        state_time = STAGE_TIMES.get(GAME_STATE)
        st = (end_time - state_time) * 1000
        YC.send(UI_HEADER.STATE(state=GAME_STATE, start_time=st, state_time=state_time))
    else:
        YC.send(UI_HEADER.STATE(state=GAME_STATE))



###########################################
# Event to Function Mappings for each Stage
###########################################

# pylint: disable=no-member


EVERYWHERE_FUNCTIONS = {
    SHEPHERD_HEADER.GET_MATCH_INFO.name: send_match_info_to_ui,
    SHEPHERD_HEADER.GET_SCORES.name: send_score_to_ui,
    SHEPHERD_HEADER.GET_STATE.name: send_state_to_ui,
    SHEPHERD_HEADER.GET_CONNECTION_STATUS.name: send_connection_status_to_ui,

    SHEPHERD_HEADER.SET_STATE.name: go_to_state,
    SHEPHERD_HEADER.ROBOT_OFF.name: disable_robot,
    SHEPHERD_HEADER.ROBOT_ON.name: enable_robot,
    SHEPHERD_HEADER.SET_ROBOT_IP.name: set_robot_ip,
    SHEPHERD_HEADER.DISCONNECT_ROBOT.name: disconnect_robot,
    SHEPHERD_HEADER.RESET_MATCH.name: reset_match,

    SHEPHERD_HEADER.TURN_LIGHT_FROM_UI.name: forward_button_light,
    SHEPHERD_HEADER.BUTTON_PRESS.name: button_pressed,
    SHEPHERD_HEADER.PAUSE_TIMER.name: pause_timer,
    SHEPHERD_HEADER.RESUME_TIMER.name: resume_timer,
    # SHEPHERD_HEADER.TURN_BUTTON_LIGHT_FROM_UI.name: forward_button_light,
    # SHEPHERD_HEADER.UPDATE_SCORE.name: update_score,
    # temporary code for exhibition, remove later
    SHEPHERD_HEADER.SET_SCORES.name: score_adjust,

}

if __name__ == '__main__':
    threading.Thread(target=pull_from_sheets, daemon=True).start()
    start()
