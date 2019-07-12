#!/usr/bin/env python3

import sys
from router import Router
from port_binding import bind_sockets


# Redefined in router.py
# class Router:
#     def __init__(self, rid, inputs, outputs):
#         """..."""
#         self.router_ID = rid
#         self.input_ports = inputs
#         self.output = outputs
#
#     def __repr__(self):
#         """Returns a printable representation of the Router object"""
#         line_count = 60
#         return_string = "-" * line_count
#         return_string += "\nROUTER CONFIGURATION\n"
#         return_string += "-" * line_count
#         return_string += "\nrouter-id: {0}\ninput-ports: {1}\noutputs: {2}\n".format(self.input_ports, self.router_ID,
#                                                                                      self.output)
#         return_string += "-" * line_count
#         return return_string


# --------------------------------------------------------------------- #
# TODO: Move to different file?
# TODO: Complete packet formats
# TODO: Create a decryption definition in the following classes (bytes -> text)
# TODO: Implement a checking method
class RipPacket:
    def __init__(self):
        """
        [Command (1 Byte)] [Version (1 Byte)] [Router ID (2 Bytes)]
        [                  RIP Entry (4 Bytes)                    ]
        """
        self.command = None
        self.version = None
        self.router_id = None
        self.rip_entry = None

    def __repr__(self):
        """Prints the contents of the packet"""
        print("Command: {0}\n"
              "Version: {1}\n"
              "Router ID: {2}\n"
              "RIP Entry: {3}").format(self.command, self.version, self.router_id, self.rip_entry)

    def create_rip(self, command, version, router_id, rip_entry):
        """Creates a RIP packet in accordance to the RIP protocol."""
        self.command = command.to_bytes(1, byteorder='big')
        self.version = version.to_bytes(1, byteorder='big')
        self.router_id = router_id.to_bytes(2, byteorder='big')
        self.rip_entry = rip_entry.to_bytes(4, byteorder='big')

    def payload(self):
        """Formats individual bytes into an entire packet to send"""
        return self.command + self.version + self.router_id + self.rip_entry


class RipEntry:
    def __init__(self):
        """
        [Address Family ID (2 Bytes)] [Zero (2 Bytes)]
        [           IPv4 Address (4 Bytes)           ] // Replace with router ID
        [           Zero (4 Bytes)                   ]
        [           Zero (4 Bytes)                   ]
        [           Metric (4 Bytes)                 ]
        Zero fields are unused since we are using RIP version 1.
        """
        self.address_id = None
        # Zero field
        self.IPv4 = None
        # Zero field
        # Zero field
        self.metric = None

    def __repr__(self):
        """Prints the contents of the packet"""
        print("Address Family ID: {0}\n"
              "IPv4 Address: {1}\n"
              "Metric: {2}").format(self.address_id, self.IPv4, self.metric)

    def create_entry(self, address_id, IPv4, metric):
        """Creates a RIP entry in accordance to the entry packet form"""
        self.address_id = address_id.to_bytes(2, byteorder='big')
        self.IPv4 = IPv4.to_bytes(4, byteorder='big')
        self.metric = metric.to_bytes(4, byteorder='big')

    def payload(self):
        """Formats individual bytes into an entire packet to send & package"""
        padding1 = bytearray(2)
        padding2 = bytearray(4)
        return self.address_id + padding1 + self.IPv4 + padding2 + padding2 + self.metric  # 20 Bytes total

# --------------------------------------------------------------------- #


def open_config():
    if len(sys.argv) != 2:
        print("USAGE: config_parse.py <input-file>")
        sys.exit()
    try:
        with open(sys.argv[1]) as config_file:
            config_data = config_file.read().splitlines()
    except FileNotFoundError:
        print("Error! Config file not found.")
        sys.exit()
    return config_parser(config_data)


def config_parser(file_data):
    """..."""
    rid, inputs, outputs = -1, [], []
    config_params = ["router-id", "input-ports", "outputs"]
    for lines in file_data:
        if lines.strip():                # Remove empty lines in config file
            lines = lines.split(" ")
            if lines[0] == config_params[0]:
                rid = lines[1]
            elif lines[0] == config_params[1]:
                for each in lines[1:]:
                    inputs.append(int(each.strip(",")))
            elif lines[0] == config_params[2]:
                for each in lines[1:]:

                    outputs.append([int(i) for i in each.strip(",").split("-")])
            else:                        # Ignore comments and other artifacts in file
                pass
        else:
            pass
    return Router(rid, inputs, outputs)


def check_config(router):
    """Checks config for integrity"""
    # TODO: Check for duplicate port numbers
    for in_port in router.input_ports:
        if int(in_port) not in range(1024, 64000):
            raise ValueError("Input port {} not in range of 1024 - 64000", in_port)
    for port_list in router.output:
        for out_port in port_list:
            if int(out_port) not in range(1024, 64000):
                raise ValueError("Output port {} not in range of 1024 - 64000", out_port)


# Run Program
if __name__ == '__main__':
    router = open_config()
    check_config(router)
    print(router)
    # bind_sockets(router)  # port_binding.py
