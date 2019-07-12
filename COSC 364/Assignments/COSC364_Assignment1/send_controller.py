"""
send_controller.py
Deals with the sending functionality of the router
"""
import socket
import time
from random import randint
from classes import *

PAUSE = False  # Pause Send Thread
HOST = socket.gethostbyname("localhost")
COMMAND = 1
VERSION = 2


def create_routing_table(router, port):
    """
    Copies dictionary to make thread-safe
    :param router: This is the main router object which contains the configuration and routing tables
    :param port: Port which the router should send the table to
    :return route_list: Routing table for the routers to build a route database of
    """
    neighbour_router_id = None
    route_list = []
    for key, value in router.connected_networks.items():
        if value[0] == port:
            neighbour_router_id = key
    address_family_id = 2
    working_dict = dict(router.routing_table)
    for peerRouterId, route in working_dict.items():
        # If the route in the table has a next hop of the router we are sending to, don't add it to table to send
        if route[1] != neighbour_router_id:  # Split Horizon
            route_list.append([address_family_id, peerRouterId, route[1], route[0]])
    return route_list


def periodic_send_control(router, base_period):
    """
    Function to send packets periodically except when the global PAUSE variable is True
    (This is to prevent ports clashing)
    Function loops after waiting for the specified time period
    :param router: This is the main router object which contains the configuration and routing tables
    :param base_period: The time between periodic sends as specified by the main controller
    """
    time.sleep(randint(0, 4))
    while True:
        if not PAUSE:
            for address in router.output_ports:
                packet = RipPacket()
                packet.create_packet(COMMAND, VERSION, int(router.router_id),
                                     create_routing_table(router, address[0]))
                packet = packet.pack_packet()
                send_packet(packet, (HOST, address[0]))
        time.sleep(base_period)


def triggered_send_control(router):
    """
    Function to send packets when triggered by the receive controller or the garbage collector
    Pauses the periodic send thread while in operation
    :param router: This is the main router object which contains the configuration and routing tables
    :except "ErrorType": FIXME: Error type?
    """
    try:
        PAUSE = True
        for address in router.output_ports:
            packet = RipPacket()
            packet.create_packet(COMMAND, VERSION, int(router.router_id), create_routing_table(router, address[0]))
            packet = packet.pack_packet()
            send_packet(packet, (HOST, address[0]))
    except Exception:  # FIXME: Proper Exception type?
        pass
    PAUSE = False


def send_packet(packet, address):
    """
    Function that sends the packet the the ports specified in the config file
    Raises an exception on error
    :param packet: The byte stream to be sent
    :param address: A tuple of the IP address to send to and the corresponding port
    :except ConnectionRefusedError: Raises a connection error if the router is unable to establish the ports
    :except socket.error: Raises a socket error if the router is unable to send the packet
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(address)
    except ConnectionRefusedError:
        raise ConnectionRefusedError("[!] ERROR: Unable to establish sockets")
    try:
        sock.sendto(packet, address)
        sock.close()
    except socket.error:
        print("[!] ERROR: Unable to send request")
