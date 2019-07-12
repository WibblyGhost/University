class Router:
    """Router Class"""

    METRIC = 0
    DELETION = False

    def __init__(self, rid, inputs, outputs):
        """Router Constructor"""
        self.router_ID = rid
        self.next_hop = rid
        self.input_ports = inputs
        self.output = outputs
        self.routing_table = {}      #dictionary with key as RID, metric and next-hop, and deletion flag
        self.routing_table = {self.router_ID: [self.METRIC, self.next_hop, self.DELETION]}
        print(self.routing_table.get(self.router_ID))

    def __repr__(self):
        """Returns a printable representation of the Router object"""
        line_count = 60
        return_string = "-" * line_count
        return_string += "\nROUTER CONFIGURATION\n"
        return_string += "-" * line_count
        return_string += "\nrouter-id: {0}\ninput-ports: {1}\noutputs: {2}\n".format(self.router_ID, self.input_ports,
                                                                                     self.output)
        return_string += "-" * line_count
        return return_string
