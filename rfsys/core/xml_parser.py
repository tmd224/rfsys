import xml.etree.ElementTree as ET


def load_components(filepath):
    """
    Top level function to load all components from the XML file into a list of dictionaries

    Component dict format:
    {'uid': 1,
     'name': 'LNA',
     'type':'Amplifier',
     'params': {
                'gain': {'name': 'gain',
                         'freqs': [10, 20, 30]
                         'values': [-0.5, -0.6, -0.65]
                         },
                'NF': {'name': 'NF',
                         'freqs': [10, 20, 30]
                         'values': [1.5, 1.55, 1.6]
                      },
                }
    }

    Args:
        filepath (str): Full filepath for the XML file

    Returns:
        comp_list (list): List of dictionaries.
    """
    root = load_xml(filepath)
    comp_list = list()
    for comp in root:
        if comp.tag == "component":
            comp_dict = parse_component(comp)
            comp_list.append(comp_dict)

    return comp_list

def load_xml(filepath):
    """
    Load XML file and return root element object

    Args:
        filepath (str): Full filepath for the XML file

    Returns:
        root: ElementTree root element object
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    return root


def parse_component(element):
    """
    Parse a component into a dictionary

    Args:
        element: component element object

    Returns:
        comp_dict (dict): Component dictionary
    """
    comp_dict = element.attrib  # return a dictionary of the attributes
    param_dict = dict()
    for param in element:
        if param.tag == "parameter":
            pdict = parse_parameter(param)
            param_dict[pdict['name']] = pdict

    comp_dict['params'] = param_dict
    return comp_dict


def parse_parameter(element):
    """
    Parse a parameter element into a dictionary
    Args:
        element: parameter element object

    Returns:
        param_dict (dict): Parameter dictionary.  Keys are name, freqs, values.
    """
    param_dict = element.attrib     # this will return a dictionary
    freqs = string_to_list(element.find("freqs").text)
    values = string_to_list(element.find("values").text)
    param_dict.update({'freqs': freqs, 'values': values})

    return param_dict


def string_to_list(string, sep=','):
    """
    Convert a comma separated string to a list of numbers

    Args:
        string (str): String to convert
        sep (str): Seperator token

    Returns:
        num_list (list):
    """
    str_list = string.split(',')
    num_list = [float(x) for x in str_list]   # convert list items to float type
    return num_list

