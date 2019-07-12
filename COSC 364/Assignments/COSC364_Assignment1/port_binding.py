import socket


"""Receiving Packets"""
def bind_sockets(router):
    server_address = "127.0.0.1"
    count = 0
    while count < len(router.input_ports):
        sock_list[count].bind((server_address, int(router.input_ports[count])))
        count += 1
        # sock.setblocking(0)
    # TODO: Error if cant bind port
    return sock_list


def receive_packet(port_list, router):
    """Function that puts the server into search mode"""
    server_ip = "127.0.0.1"
    try:
        sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in router.input_ports]
        counter = 0
        for sock in sock_list:
            sock.bind((server_ip, router.input_ports[counter]))
            sock.setblocking(0)
            counter += 1
    except OSError:
        print("Could not open and/or bind specified server ports.\n---Exiting---")
    print("Sockets connected.\nListening on ports _ for incoming transmissions.\n...")




"""Sending Packets"""
def send_packet(packet, server_address):
    """Function that sends the packet"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("Could not establish an outgoing connection.\n---Exiting---")
    sock.sendto(packet, server_address)
    # Recieve any other packets?
    # Close socket
    # sock.close()