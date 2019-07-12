#!/usr/bin/env python3
"""
controller.py
This file will deal with threading operations and act as a core controller for the router
"""
import os
import threading
import config_parse
import receive_controller
import send_controller
import timers

DEBUG = False
DIVISOR = 12  # Used for testing to speed up network convergence
TIMER = 30 // DIVISOR
TIMEOUT = 180 // DIVISOR
DELETE_TIMER = 120 // DIVISOR
CLI_REFRESH_RATE = 1

# Main function for which the program initially starts from
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    router = config_parse.open_config()
    config_parse.check_config(router)
    router.route_timeout = TIMEOUT
    router.print_router_config()
    router.print_routing_table()
    receive = threading.Thread(target=receive_controller.receive_packet, args=(router, TIMEOUT))
    periodic_send = threading.Thread(target=send_controller.periodic_send_control, args=(router, TIMER))
    timeout_timer = threading.Thread(target=timers.timeout, args=(router, TIMEOUT))
    cli_update = threading.Thread(target=timers.cli_refresh, args=(router, CLI_REFRESH_RATE))
    cli_update.start()
    periodic_send.start()
    receive.start()
    timeout_timer.start()
