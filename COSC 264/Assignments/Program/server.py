"""
COSC 264 - Assignment 1
Creation Date: 30/7/18
Name: Zachary Sanson
Student ID: 58520526
File: Server.py
"""
#   Note printing my program into a PDF makes a mess of my formatting


import socket
import select
import datetime


class DtRequest:
    """Class for a DT Request Packet"""
    def __init__(self):
        self.magicNo = 0x0000.to_bytes(2, byteorder='big')         # 16-bit
        self.packetType = 0x0000.to_bytes(2, byteorder='big')      # 16-bit
        self.requestType = 0x0000.to_bytes(2, byteorder='big')     # 16-bit 0x0001 or 0x0002

    def __str__(self):
        """Representation of our packet in string form"""
        return str(self.magicNo + self.packetType + self.requestType)

    def convert_bin(self, bin_string):
        """Converts a binary string to a DT Response type"""
        if len(bin_string) != 6:
            raise ValueError("DtRequest received an incorrect packet length.\n---Exiting---")
        self.magicNo = bin_string[:2]
        self.packetType = bin_string[2:4]
        self.requestType = bin_string[4:6]

    def check_request(self):
        """Checks if packet is a valid request packet"""
        # We do not need to check for packet length = 6 as it is covered in convert_bin
        magic_n, p_type = 0x497E.to_bytes(2, byteorder='big'), 0x0001.to_bytes(2, byteorder='big')
        requests = [0x0001.to_bytes(2, byteorder='big'), 0x0002.to_bytes(2, byteorder='big')]
        if self.magicNo == magic_n and self.packetType == p_type and self.requestType in requests:
            return True
        else:
            return False


class DtResponse:
    """Class for a DT Response Packet"""
    def __init__(self):
        self.magicNo = 0x497E.to_bytes(2, byteorder='big')         # 16-bit
        self.packetType = 0x0002.to_bytes(2, byteorder='big')      # 16-bit
        self.languageCode = 0x0000.to_bytes(2, byteorder='big')    # 16-bit, 0x0001 or 0x0002 or 0x0003
        self.year = 0x0000.to_bytes(2, byteorder='big')            # 16-bit, year < 2100
        self.month = 0x0000.to_bytes(1, byteorder='big')           # 8-bit, range(1, 12)
        self.day = 0x0000.to_bytes(1, byteorder='big')             # 8-bit, range(1, 31)
        self.hour = 0x0000.to_bytes(1, byteorder='big')            # 8-bit, range(0, 23)
        self.minute = 0x0000.to_bytes(1, byteorder='big')          # 8-bit, range(0, 59)
        self.length = 0x0000.to_bytes(1, byteorder='big')          # 8-bit
        self.text = 0x0000.to_bytes(1, byteorder='big')            # ?-bit, gets re-declared when class is created

    def __str__(self):
        """Representation of our packet in string form"""
        return str(self.magicNo + self.packetType + self.languageCode + self.year + self.month + self.day + \
                   self.hour + self.minute + self.length + self.text)

    def packet(self):
        """Prepares DT Response packet for transfer"""
        # Returns a bytearray that will be sent to clients
        return self.magicNo + self.packetType + self.languageCode + self.year + self.month + self.day + self.hour + \
            self.minute + self.length + self.text


def user_input():
    """Prompts user for input for setup"""
    server_input = [None, None, None]
    # Defining either an IP address or a hostname of the server
    usr_in = input("Enter an IP address or hostname for the server to run on: ")
    try:
        socket.getaddrinfo(usr_in, 00000)  # Port doesn't matter for checking address
        machine_ip = usr_in
    except OSError:
        print("ValueError: encountered invalid input for a server address.\n---Exiting---")
    # Defining the three port numbers to run the server on
    for count in range(0, 3):
        interface = input("Input value for port {}: ".format(count + 1))
        if int(interface) not in range(1024, 64000):
            raise ValueError("entered port number is out of range 1,024 - 64,000.\n---Exiting---")
        if int(interface) in server_input:
            raise AssertionError("port number already used within the machine.\n---Exiting---")
        server_input[count] = int(interface)
    return server_input, machine_ip


def get_string(language, text_type):
    """Creates the response string in accordance to the clients wishes"""
    # Pretty straight forward, deciphering what language and string to use for our packet
    date = datetime.datetime.now()
    year, month, day, hour, minute = date.year, date.month, date.day, date.hour, date.minute
    type_date = 0x0001.to_bytes(2, byteorder='big')
    if language == 0x0001:
        language_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                           'August', 'September', 'October', 'November', 'December']
        if text_type == type_date:
            language_string = "Today's date is {} {}, {}".format(language_months[month - 1], day, year)
        else:
            language_string = "The current time is {}:{}".format(hour, minute)
    elif language == 0x0002:
        language_months = ['Kohitatea', 'Hui-tanguru', 'Poutu-te-rangi', 'Paenga-whawha', 'Haratua', 'Pipiri',
                           'Hongongoi', 'Here-turi-koka', 'Mahuru', 'Whiringa-a-nuku', 'Whiringa-a-rangi',
                           'Hakihea']
        if text_type == type_date:
            language_string = "Ko te ra o tenei ra ko {} {} {}".format(language_months[month - 1], day, year)
        else:
            language_string = "Ko te wa o tenei wa {}:{}".format(hour, minute)
    else:
        language_months = ['Januar', 'Februar', 'Marz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September',
                           'Oktober', 'November', 'Dezember']
        if text_type == type_date:
            language_string = "Heute ist der {}. {} {}".format(language_months[month - 1], day, year)
        else:
            language_string = "Die Uhrzeit ist {}:{}".format(hour, minute)
    return language_string, date


def create_dt_response(language, date, string, text_type):
    """Creates/updates the DT Response packet"""
    dt_response = DtResponse()
    dt_response.languageCode = language.to_bytes(2, byteorder='big')
    # If text is date format
    if text_type == 0x0001.to_bytes(2, byteorder='big'):
        dt_response.year = date.year.to_bytes(2, byteorder='big')
        dt_response.month = date.month.to_bytes(1, byteorder='big')
        dt_response.day = date.day.to_bytes(1, byteorder='big')
    # time otherwise
    else: # Else is fine as the packet should have passed a check
        dt_response.hour = date.hour.to_bytes(1, byteorder='big')
        dt_response.minute = date.minute.to_bytes(1, byteorder='big')
    # Check for length of text |T| >= 255
    if len(string.encode('utf-8')) < 255:
        dt_response.text = string.encode('utf-8')
    else:
        raise ValueError("Text field is not within 255 bytes.\n---Exiting---")
    dt_response.length = len(dt_response.text).to_bytes(1, byteorder='big')
    return dt_response


def packet_processing(packet, address, sock, port_no, port):
    """Checks packet for integrity then sends out a response"""
    # Creating a DtRequest packet and performing checks on the packet
    dt_request = DtRequest()
    dt_request.convert_bin(packet)
    if dt_request.check_request():
        print("Packet has passed the required DT Request integrity checker.\nGenerating a DT Response packet\n...")
        text_type = dt_request.requestType
        # Finds what language to use from the port we received the packet from
        if port_no == 0:
            language = 0x0001
        elif port_no == 1:
            language = 0x0002
        elif port_no == 2:
            language = 0x0003
        # Creating text for the packet
        string, date = get_string(language, text_type)
        # Creating DT Response packet
        dt_response = create_dt_response(language, date, string, text_type)
        print("DT Response packet created.\nSending packet to {}:{} from port {}.\n...".format(address[0], address[1], port))
        sock.sendto(dt_response.packet(), address)
        print("Response successfully sent to {}:{}.\n...".format(address[0], address[1]))
    else:
        print("Received packet did not pass the DT Request integrity checker.\n---Ignoring Packet---")


def receive(port_list, server_ip):
    """Sets up server sockets and checks for incoming data"""
    print("Setting up sockets {}, {}, {} on {}.\n...".format(port_list[0], port_list[1], port_list[2], server_ip))
    try:
        # Setting up sockets for server to run on
        sock1, sock2, sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM), \
                              socket.socket(socket.AF_INET, socket.SOCK_DGRAM), \
                              socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockets, counter = [sock1, sock2, sock3], 0
        # Binding each socket to their respective port
        for sock in sockets:
            sock.bind((server_ip, port_list[counter]))
            sock.setblocking(0)
            counter += 1
    except OSError:
        print("Could not open and/or bind specified server ports.\n---Exiting---")
    print("Sockets connected.\nListening on ports {}, {}, {} for incoming transmissions.\n...".format(
        port_list[0], port_list[1], port_list[2]))
    while True:  # Indefinitely checks for incoming packets
        # Waits until a packet arrives on any port
        read_list, _, _ = select.select(sockets, [], [])
        for readable_socket in read_list:
            received_packet, address = readable_socket.recvfrom(60)
            port_no = port_list.index(readable_socket.getsockname()[1])
            print("Found packet on port {} from {}:{}, checking packet for integrity.\n...".format(port_list[port_no], address[0], address[1]))
            packet_processing(received_packet, address, readable_socket, port_no, port_list[port_no])


def main():
    """Main call for the server program"""
    port_list, server_ip = user_input()
    receive(port_list, server_ip)


main()
