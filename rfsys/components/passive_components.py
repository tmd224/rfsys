from .base_component import Component


class PassiveComponent(Component):
    def __init__(self, uid, name):
        """
        Base class for all passive components

        Args:
            uid (str): Unique ID
            name (str: Component name
        """
        super().__init__(uid, name)

    def add_parameter(self, name, freqs, values, **kwargs):
        """

        Args:
            name:
            freqs:
            values:
            **kwargs:

        Returns:

        """
        if name == 'gain':
            # gain is being updated, so we'll automatically add a NF parameter at the same freq
            super().add_parameter(name, freqs, values, **kwargs)
            nf_values = [x * -1 for x in values]
            super().add_parameter('NF', freqs, nf_values)


class Filter(PassiveComponent):
    def __init__(self, uid, name):
        super().__init__(uid, name)