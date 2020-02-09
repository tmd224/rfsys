from .passive_components import Filter
from .active_components import Amplifier

VALID_PASSIVE = [
    'Filter',
    'Attenuator',
    'Mixer',
    'Coupler',
    'Tap',
    'Splitter',
]

VALID_ACTIVE = [
    'Amplifier',
    'ActiveMixer',
    'Switch',
]

VALID_COMPONENTS = VALID_PASSIVE + VALID_ACTIVE


def component_builder(comp_dict):
    """
    This function builds an actual component object from a dictionary as parsed from the xml_parser

    Args:
        comp_dict (dict): Component dictionary

    Returns:
         comp (Component): Component object of the correct type
    """
    uid = comp_dict['uid']
    name = comp_dict['name']
    comp_type = comp_dict['type']
    if comp_type in VALID_COMPONENTS:
        # valid component
        classHandle = globals()[comp_type]  # get handle to class name
        compObj = classHandle(uid, name)    # create instance of the component class

        # add all parameters to the component object
        params_dict = comp_dict['params']
        for key, val in params_dict.items():
            compObj.add_parameter(**val)

        return compObj
    else:
        raise Exception("Invalid component type ({}). Valid components: {}".format(comp_type, VALID_COMPONENTS))
