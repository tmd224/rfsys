from .base_component import Component


class ActiveComponent(Component):
    def __init__(self, uid, name):
        """
        Base class for all passive components

        Args:
            uid (str): Unique ID
            name (str: Component name
        """
        super().__init__(uid, name)


class Amplifier(ActiveComponent):
    def __init__(self, uid, name):
        super().__init__(uid, name)