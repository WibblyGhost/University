"""
config_parse.py
This file deals with unpacking a .txt file and creating routers based on the file arguments
"""
import sys
from classes import *


def open_config():
    """
    Opens config file specified in the command line arguments and reads each line
    :return config_parser: String containing all lines in the config file
    :except FileNotFoundError: Raises file not found error if the parser cannot locate the given file
    """
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
    """
    Parses information from the data extracted from the config file and returns
    a router Object constructed with the parsed data
    :return Router: Constructed Router object
    """
    inputs, outputs = [], []
    rid = -1
    config_params = ["router-id", "input-ports", "outputs"]
    for lines in file_data:
        if lines.strip():  # Remove empty lines in config file
            lines = lines.split(" ")
            if lines[0] == config_params[0]:
                rid = lines[1]
            elif lines[0] == config_params[1]:
                for each in lines[1:]:
                    inputs.append(int(each.strip(",")))
            elif lines[0] == config_params[2]:
                for each in lines[1:]:
                    outputs.append([int(i) for i in each.strip(",").split("-")])
            else:  # Ignore comments and other artifacts in file
                pass
        else:
            pass
    return Router(rid, inputs, outputs)


def check_config(router):
    """
    Checks Router configuration for integrity, as per assignment specification
    :param router: This is the main router object which contains the configuration and routing tables
    :except ValueError: Raises value error if duplicate ports are found in the config
    """
    for in_port in router.input_ports:
        if router.input_ports.count(in_port) > 1:
            raise ValueError("Found duplicate port ({0}) in the routers inputs.".format(in_port))
        elif in_port not in range(1024, 64000):
            raise ValueError("Input port {0} not in range of 1024 - 64000".format(in_port))
    out_ports = [port[0] for port in router.output_ports]
    for port in out_ports:
        if out_ports.count(port) > 1:
            raise ValueError("Found duplicate port ({0}) in the routers outputs.".format(port))
        if port not in range(1024, 64000):
            raise ValueError("Output port {0} not in range of 1024 - 64000".format(port))
