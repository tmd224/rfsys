import re


class Part:
    def __init__(self, refdes, uid, port):
        """
        Container to hold part info within a net definition
        Args:
            RefDes:
            uid:
            port:
        """
        self.refdes = refdes
        self.uid = uid
        self.port = port


class Net:
    def __init__(self, input, output):
        """
        Container to define Part objects as a net connection

        Args:
            input (Part): Input Part of net
            output (List): List of Part objects as output connections of net
        """
        self.input = input
        self.output = output


class Source:
    def __init__(self, id):
        self.id = id


class Sink:
    def __init__(self, id):
        self.id = id

def parse_net(line):
    """
    Parse a net string into individual pieces
    Args:
        line:

    Returns:
    """
    if line[-1] == ';':
        line = line[:-1]  # pop off trailing semi-colon

    components = line.split(';')    # split each components up
    input_str = components[0]   # first element is the input component
    input_part = parse_part(input_str)


    output_list = list()
    for x in range(1, len(components)):
        # create Part objects for all of the output nodes
        output_str = components[x]
        output_part = parse_part(output_str)
        output_list.append(output_part)

    net = Net(input_part, output_list)
    return net


def parse_part(part_str):
    part_dict = dict()
    match = re.search("([a-zA-Z0-9]+)-([a-zA-Z0-9]+).([0-9]+)", part_str)
    if match:
        part_dict['refdes'] = match.group(1)
        part_dict['uid'] = match.group(2)
        part_dict['port'] = match.group(3)
        part = Part(**part_dict)
        return part
    else:
        # check for a built-in source or sink component
        match = re.search("([a-zA-Z]+).([0-9]+)", part_str)

        if match:
            if match.group(1).upper() == "SOURCE":
                return Source(match.group(2))
            elif match.group(1).upper() == "SINK":
                return Sink(match.group(2))

    raise Exception("Netlist parse error - part string is invalid ({})".format(part_str))


if __name__=="__main__":
    filepath = 'netlist_test.txt'
    with open(filepath) as fp:
        lines = fp.readlines()

    net_list = list()
    for line in lines:
        l = line.strip()
        if len(l) > 0:
            if l[0] == "#":
                # print("Comment: {}".format(l))
                pass
            else:
                print("Valid Line: {}".format(l))
                net_list.append(parse_net(l))

    # parse overall netlist into linear paths
