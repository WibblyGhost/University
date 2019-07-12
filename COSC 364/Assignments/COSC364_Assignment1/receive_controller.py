"""
receive_controller.py
Deals with the receiving functionality of the router
"""
import select
import socket
import controller
import send_controller
import timers
from classes import *


def receive_packet(router, timeout_len):
    """
    Function that puts the router into a continuous search for incoming packets
    :param router: This is the main router object which contains the configuration and routing tables
    :param timeout_len: Length of time it takes for a route to timeout as specified in the main controller
    :except OSError: Raises an OS error if ports could not be bound
    """
    server_ip = "127.0.0.1"
    sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in router.input_ports]
    try:
        counter = 0
        for sock in sock_list:
            sock.bind((server_ip, router.input_ports[counter]))
            sock.setblocking(False)
            counter += 1
    except OSError:
        print("Could not open and/or bind specified server ports.\n---Exiting---")
    print("Sockets connected.\nListening on ports {0} for incoming transmissions.\n...".format(router.input_ports))
    while True:
        readable, writable, exceptional = select.select(sock_list, [], [])
        for connection in readable:
            accept_connection(connection, router)


def accept_connection(connection, router):
    """
    Receives the packet from the socket and calls the packet verification function
    If verification fails, an error is thrown
    :param connection: Ports which the router is listening on
    :param router: This is the main router object which contains the configuration and routing tables
    """
    data, address = connection.recvfrom(1024)
    received_packet = RipPacket()
    received_packet.unpack_packet(data)
    received_packet.check_packet()
    if not received_packet.drop_packet:
        update_routing_table(router, received_packet)


def update_routing_table(router, received_packet):
    """
    Updates Router routing table entries with that of received packet
    :param received_packet: Received byte stream to convert
    :param router: This is the main router object which contains the configuration and routing tables
    """
    trigger_send = False
    working_dict = dict(router.routing_table)  # Thread Safety
    received_rid = received_packet.router_id
    for (_, destination_rid, next_hop, metric) in received_packet:
        timestamp = datetime.datetime.now().timestamp()
        new_metric = min((metric + router.connected_networks.get(received_rid)[1]), 16)
        existing_metric = 16 if working_dict.get(destination_rid) is None else working_dict.get(destination_rid)[0]
        # If destination_rid not in router.connected_networks
        if destination_rid not in working_dict:
            if new_metric < 16:
                working_dict.update({destination_rid: [new_metric, received_rid, False, timestamp]})
        elif (working_dict.get(destination_rid)[1] == received_rid or
              new_metric < existing_metric):
            if new_metric <= existing_metric and new_metric < 16:
                working_dict.update({destination_rid: [new_metric, received_rid, False, timestamp]})
            elif new_metric == 16:
                prev_time = working_dict.get(destination_rid)[3]
                working_dict.update({destination_rid: [16, received_rid, True, prev_time]})
                trigger_send = True
    router.routing_table = dict(working_dict)  # Copy dictionary back into place
    if trigger_send:
        send_controller.triggered_send_control(router)
        timers.garbage_collection(router, controller.DELETE_TIMER)
