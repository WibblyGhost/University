"""
timers.py
This file just defines a timeout period used by the routers for timeouts and other timed events
"""
import datetime
import os
import threading
import time
import controller
import send_controller


def timeout(router, timeout_len):
    """
    Handles timeout thread and triggers an update and garbage collection if a link times out
    :param router: This is the main router object which contains the configuration and routing tables
    :param timeout_len: Length of time it takes for a route to timeout as specified in the main controller
    """
    while True:
        trigger_send = False
        now = datetime.datetime.now().timestamp()
        key_list = []
        working_dict = dict(router.routing_table)
        for peerId, (_, _, garbage, timeout) in working_dict.items():
            if peerId != router.router_id:  # Prevent deleting self from table.
                if int(now - timeout) >= timeout_len:
                    garbage = True
                    key_list.append(peerId)
                    trigger_send = True
        for each in key_list:
            working_dict[each][2] = True
            working_dict[each][0] = 16
        router.routing_table = dict(working_dict)  # Copy dictionary back into place
        if trigger_send:
            send_controller.triggered_send_control(router)
            garbage_thread = threading.Thread(target=garbage_collection, args=(router, controller.DELETE_TIMER))
            garbage_thread.start()
        time.sleep(1)


def cli_refresh(router, refresh):
    """
    Refreshes the display every second as long as the Global DEBUG is not set
    :param router: This is the main router object which contains the configuration and routing tables
    :param refresh: Length of time before the display refreshes as specified in the main controller
    """
    while True:
        time.sleep(refresh)
        if not controller.DEBUG:
            os.system('cls' if os.name == 'nt' else 'clear')
        router.print_routing_table()


def garbage_collection(router, period):
    """
    Cleans the routing table of expired routes after the timer has expired
    :param router: This is the main router object which contains the configuration and routing tables
    :param period: Length of time after timeout until the garbage collection starts as specified
    in the main controller
    """
    time.sleep(period)
    key_list = []
    working_dict = dict(router.routing_table)
    for key, value in working_dict.items():
        if key != router.router_id and value[2]:
            key_list.append(key)
    for key in key_list:
        del working_dict[key]
    router.routing_table = dict(working_dict)  # Copy dictionary back into place
