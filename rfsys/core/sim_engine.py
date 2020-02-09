import math
from ..components.base_component import ComponentData


class CascadeEngine:

    def __init__(self, comp_list, **kwargs):
        """
        Cascaded simulation engine for cascading various RF parameters
        Args:
            **kwargs:
        """
        self.comp_list = comp_list
        self.comp_data = list()

    def add_component_data(self, uid, name):
        """
        Add or retreive a component data object
        Args:
            uid (str): Unique ID
            name (name): Component name

        Returns:
            (ComponentData)
        """
        for comp in self.comp_data:
            if comp.uid == uid:
                return comp

        # if we didn't find the uid, add a new ComponentData object to the list
        comp_data = ComponentData(uid, name)
        self.comp_data.append(comp_data)
        return comp_data

    def run(self, freq):

        for idx, comp in enumerate(self.comp_list):
            comp_data = self.add_component_data(comp.uid, comp.name)

            self.cascade_gain(comp, comp_data, idx, freq)
            self.cascade_nf(comp, comp_data, idx, freq)

    def cascade_gain(self, comp, comp_data, idx, freq):
        """
        calculate the cascaded gain for the current stage

        Args:
            comp (Component): Current component object
            comp_data (ComponentData): Corresponding component data object
            idx (int): Current index in the component list
            freq (float): Current simulation frequency in MHz

        Returns:
            None
        """
        if idx == 0:
            prev_gain = 0
        else:
            prev_comp = self.comp_data[idx-1]
            prev_gain = prev_comp.get_value('gain', freq)

        gain = prev_gain + comp.get_value('gain', freq)
        comp_data.update_parameter('gain', freq, gain)

    def cascade_nf(self, comp, comp_data, idx, freq):
        """
        calculate the cascaded NF for the current stage

        Args:
            comp (Component): Current component object
            comp_data (ComponentData): Corresponding component data object
            idx (int): Current index in the component list
            freq (float): Current simulation frequency in MHz

        Returns:
            None
        """
        if idx == 0:
            prev_gain = 0
            prev_nf = 0
        else:
            prev_comp = self.comp_data[idx-1]
            prev_gain = prev_comp.get_value('gain', freq)
            prev_nf = prev_comp.get_value('NF', freq)

        current_nf = comp.get_value('NF', freq)

        prev_nf_linear = self._get_linear_value(prev_nf)
        gain = self._get_linear_value(prev_gain)
        current_nf_linear = self._get_linear_value(current_nf)
        nf_linear = prev_nf_linear + ((current_nf_linear - 1) / gain)
        casc_nf = round(self._get_db_value(nf_linear), 2)
        comp_data.update_parameter('NF', freq, casc_nf)

    @staticmethod
    def _get_linear_value(value):
        """
        Convert a value in dB to it's linear equivalent

        Args:
            value (float): value in dB

        Returns:
            (float): value in linear units
        """
        return 10**(value / 10.0)

    @staticmethod
    def _get_db_value(value):
        """
        Convert a value in linear units to a dB equivalent

        Args:
            value (float): value in linear units

        Returns:
            (float): value in dB units
        """
        return 10 * math.log10(value)





