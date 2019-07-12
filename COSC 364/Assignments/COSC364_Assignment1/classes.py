"""
classes.py
Defines three classes:
    Router, which holds information about the router
    RipEntry, which hold the data for each individual rip entry
    RipPacket, which holds the entire packet (including the rip entries)
"""
import datetime
from struct import *
from prettytable import PrettyTable


class Router:
    """
    Router Class - This is the main router object and contains the configuration data
    and manages the router's Routing Table(RT)
    """

    def __init__(self, rid, inputs, outputs):
        """
        Initialisation of the Router class which holds all information regarding routing tables, timeouts and more
        Router Constructor
        :param rid: Router object ID
        :param inputs: List of the input ports of the router
        :param outputs: List containing input ports of peer routers, metric and the peer router id
        """
        self.router_id, self.next_hop = int(rid), int(rid)
        self.input_ports = inputs
        self.output_ports = outputs
        self.metric = 0
        self.garbage = False
        self.timeout, self.route_timeout = None, None
        self.connected_networks = {}
        self.routing_table = {}  # Dictionary with key as RID, metric and next-hop, and deletion flag
        self.routing_table = {self.router_id: [self.metric, self.next_hop, self.garbage, self.timeout]}
        for entry in self.output_ports:
            self.connected_networks.update({entry[2]: [entry[0], entry[1]]})

    def print_routing_table(self):
        """
        Prints the router's current routing table using the PrettyTable formatter
        """
        table = PrettyTable(['Router ID', 'Metric', 'Next Hop', 'Garbage', 'Timeout'])
        for key, value in self.routing_table.items():
            now = datetime.datetime.now().timestamp()
            table.add_row([key, value[0], value[1], value[2],
                           int(self.route_timeout - (now - value[3])) if value[3] is not None else None])
        print("+---------------------------------------------------+")
        print("|                   Router ID: {0}                    |".format(self.router_id))
        print(table)

    def print_router_config(self):
        """
        Prints the router configuration data if a table form
        """
        line_count = 40
        line_special = "+" + ("-" * line_count) + "+"
        table = PrettyTable(["Parameter", "Value"])
        table.add_row(["Router ID", self.router_id])
        table.add_row(["Input Ports", ", ".join(map(str, self.input_ports))])
        title = "|          ROUTER CONFIGURATION          |\n"
        output_table = PrettyTable(['Output Port', 'Metric', 'Peer ID'])
        for value in self.output_ports:
            output_table.add_row([value[0], value[1], value[2]])
        print(line_special + '\n' + title + line_special)
        print(table)
        print(output_table)


# --------------------------------------------------------------------- #


# Sub-Class
class RipEntry:
    """
    Class to deal with packing and unpacking RIP Entries into the RIP Packet
    Contains functions to create, pack (into byte stream), unpack (from byte stream), printing and indexing
    """

    def __init__(self, input_bytes=None):
        """
        Initialisation of our RipEntry class can receive a byte stream to convert into an object or raw input
        RipEntry is a sub-class of RipPacket and is used within the creation of RipPackets
        :param input_bytes: A byte stream to be converted from raw

        [Address Family ID (2 Bytes)] [Zero (2 Bytes)]
        [           Router ID (4 Bytes)              ]
        [           Zero (4 Bytes)                   ]
        [           Next Hop (4 Bytes)               ]
        [           Metric (4 Bytes)                 ]
        """
        if input_bytes:
            self.unpack_entry(input_bytes)
        else:
            self.address_family_id = None
            self.rid = None
            self.next_hop = None
            self.metric = None
        self.padding_1 = 0
        self.padding_2 = 0

    def __str__(self):
        """
        Prints the contents of the RipEntry class
        :return string: Representation of the RipEntry in list form
        """
        return "[{0}, {1}, {2}, {3}]".format(self.address_family_id, self.rid, self.next_hop, self.metric)

    def print_entry(self):
        """
        Prints the representation of the RipEntry class
        :return repr: Returns a representation of the RipEntry
        """
        return "\tAddress ID: {0}\n" \
               "\tZero: {1}\n" \
               "\tRouter ID: {2}\n" \
               "\tZero: {3}\n" \
               "\tNext Hop: {4}\n" \
               "\tMetric: {5}".format(self.address_family_id, self.padding_1, self.rid, self.padding_2,
                                      self.next_hop, self.metric)

    def __len__(self):
        """
        Redefines the length command for the RipEntry class
        :return length: Returns the length of the Entry packet
        """
        return len(self.entry_payload())

    def __getitem__(self, index):
        """
        Redefines the __getitem__ function to allow for indexing
        :param index: Index of item in 'self'
        :return items[index]: Returns an element of the 'self' class at given index
        """
        items = [self.address_family_id, self.rid, self.next_hop, self.metric]
        return items[index]

    def create_entry(self, data):
        """
        Updates/creates the RipEntry class fields when new information is present
        :param data: An input list of size 4 to be converted to the object
        """
        self.address_family_id, self.rid, self.next_hop, self.metric = data[0], data[1], data[2], data[3]

    def unpack_entry(self, byte_string):
        """
        Updates the RipEntry class fields when new information is present
        :param byte_string: Unpacks a byte string and converts it to a RipEntry object
        """
        data = unpack(">hhiiii", byte_string)
        self.address_family_id, self.rid, self.next_hop, self.metric = data[0], data[2], data[4], data[5]

    def entry_payload(self):
        """
        Converts the RipEntry class object into a byte stream
        :return byte_stream: Returns a byte stream made from the RipEntry object
        """
        return pack(">hhiiii", self.address_family_id, self.padding_1, self.rid, self.padding_2, self.next_hop,
                    self.metric)


# Super-Class
class RipPacket(RipEntry):
    """
    Class to deal with packing and unpacking RIP Packets
    Contains functions to create, pack (into byte stream), unpack (from byte stream),
    checking, printing and indexing
    """

    def __init__(self, input_bytes=None):
        """
        Initialisation of our RipPacket class can receive a byte stream to convert into an object or raw input
        RipPacket is a super-class of RipEntry which is used when creating packets
        :param input_bytes: A byte stream to be converted from raw

        [Command (1 Byte)] [Version (1 Byte)] [Router ID (2 Bytes)]
        [                  RIP Entry (20 Bytes)                   ]
        """
        super().__init__()  # Superclass / Parent of RipEntry
        self.drop_packet = False
        self.rip_entries = []
        if input_bytes:
            self.unpack_packet(input_bytes)
        else:
            self.command = None
            self.version = None
            self.router_id = None

    def __str__(self):
        """Prints the contents of the RipPacket class
        :return repr: Representation of the RipPacket
        """
        return "\nCommand: {0}\n" \
               "Version: {1}\n" \
               "Router ID: {2}\n" \
               "RIP Entries: {3}".format(self.command, self.version, self.router_id, self.str_rip_entries())

    def str_rip_entries(self):
        """
        Prints the representation of all the RipEntries
        :return string: Returns a representation of each RipEntry contained in the packet
        """
        string = ""
        for item in self.rip_entries:
            string += "\n" + item.print_entry() + "\n"
        return string

    def __len__(self):
        """
        Redefines the length command for the RipPacket class
        :return length: Returns the length of the entire RipPacket
        """
        return len(self.pack_packet())

    def __getitem__(self, index):
        """
        Redefines the __getitem__ function to allow for indexing
        :param index: Index of item in 'self'
        :return items[index]: Returns indexed RipEntry from the list of RipEntries contained in 'self'
        """
        return self.rip_entries[index]

    def create_packet(self, command, version, router_id, entry_table):
        """
        Creates a packet from the RipPacket class, including all the RipEntries also contained within 'self'
        :param command: Command field to update
        :param version: Version field to update
        :param router_id: Router ID field to update
        :param entry_table: List of RipEntries to update
        """
        if None in (command, version, router_id) or None in entry_table:
            self.drop_packet = True
            print("create_packet has received 'None' arguments.\n"
                  "Dropping packet.")
        self.command, self.version, self.router_id = command, version, router_id
        for item in entry_table:
            entry = RipEntry()
            entry.create_entry(item)
            self.rip_entries.append(entry)

    def pack_packet(self):
        """
        Creates a byte stream from the RipPacket class, including all the RipEntries also contained within 'self'
        :return packet: A complete representation of the RipPacket's byte stream
        """
        packet = pack(">bbh", self.command, self.version, self.router_id)
        for item in self.rip_entries:
            packet += item.entry_payload()
        return packet

    def unpack_packet(self, input_bytes):
        """
        Updates the RipPacket object fields from a stream of bytes
        :param input_bytes: Unpacks a byte string and converts it to a RipPacket object
        """
        count, packet_len = 4, len(input_bytes)
        # Check that entry packets are 20 bytes each
        if (packet_len - 4) % 20 != 0:
            self.drop_packet = True
            print("One of the entry packets are not of size 20 bytes.\n"
                  "Dropping packet.")
        else:
            self.command, self.version, self.router_id = unpack(">bbh", input_bytes[:4])
            # For each 20 bytes, split into a list of RipEntries
            while count < packet_len:
                entry = RipEntry(input_bytes[count:count + 20])
                self.rip_entries.append(entry)
                count += 20
            if self.check_packet() is not None:
                self.drop_packet = True
                print(self.check_packet())

    def check_packet(self):
        """
        Checks the converted message for errors when converting into the RipPacket class
        Checks for None fields, header length, command fields, version fields
        and RipEntries (address_family_id & metrics)
        :return string: Returns a string representation of th error that occurred if failing any checks
        """
        # Checking within the RipPacket Header
        if None in [self.command, self.version, self.router_id]:
            return "Error creating packet 'None' fields exist.\n" \
                   "Dropping packet."
        if self.__len__() < 4:
            return "RIP header is an incorrect size.\n" \
                   "Dropping packet."
        elif 2 < self.command < 0:  # 1 -> Request, 2 -> Response
            return "Command field ({0}) not within 1 - 2.\n" \
                   "Dropping packet.".format(self.command)
        elif self.version != 2:  # 2 -> RIP Format
            return "Version field ({0}) does not equal 2.\n" \
                   "Dropping packet.".format(self.version)
        # Checking all RipEntries
        if len(self.rip_entries) > 0:
            for item in self.rip_entries:
                if item.address_family_id != 2:
                    return "RipEntry version field ({0}) does not equal 2.\n" \
                           "Dropping packet.".format(item.address_family_id)
                elif item.metric < 0:
                    return "Metric field ({0}) is less than 0.\n" \
                           "Dropping packet.".format(item.metric)
        return None

# --------------------------------------------------------------------- #
