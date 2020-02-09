import random
import numpy as np
from ..core.errors import validate_arg, verify_kwargs


class Component:

    def __init__(self, uid, name):
        """
        Base class for all components.  Defines template behavior for all types of components

        Args:
            uid (str): unique ID
            name (str): Name of component
        """
        self.uid = str(uid)
        self.name = name
        self._parameters = dict()

    def add_parameter(self, name, freqs, values, **kwargs):
        """
        This method will add a parameter to the component object.  It will create a Parameter object

        Args:
            name (str): name of parameter
            freqs (list): list of frequency values in MHz
            values (list): list of parameter values for each freq in the list
            **kwargs: Arguments for Tolerance class
        """
        if name in self._parameters.keys():
            raise ValueError("Parameter name ({}) already exists in Component ({})".format(name, self.name))
        if not isinstance(freqs, list):
            freqs = list(freqs)

        if not isinstance(values, list):
            values = list(values)

        if len(freqs) != len(values):
            raise ValueError("Length of parameter freqs ({}) does not equal length of values ({})"
                             .format(freqs, values))

        param = Parameter(name, freqs, values, **kwargs)
        self._parameters[name] = param

    def get_parameter(self, name):
        """
        Method to retrieve a component parameter object

        Args:
            name (str): parameter name

        Returns:
            obj: parameter object
        """
        if name not in self._parameters.keys():
            raise ValueError("Component ({}) has no Parameter name ({})".format(self.name, name))

        return self._parameters[name]

    def get_value(self, param, freq):
        """
        Method to get a parameter value for a particular frequency
        Args:
            param (str): parameter name
            freq (float): Frequency in MHz

        Returns:
            value (float):
        """
        p = self.get_parameter(param)
        value = p.get_value(freq)
        return value


class Parameter:

    def __init__(self, name, freqs, values, **kwargs):
        """
        Args:
            name (str): parameter name
            freqs (list): list of frequency values in MHz
            values (list): parameter value as function of frequency
            **kwargs (dict): keyword args

        Keyword Args:
            tol (str): type of tolerance [dB or per]
            dist (str): Distribution type (uniform, normal)
            mean (float): mean value of parameter
            lower_limit (float): lower limit of parameter range
            upper_limit float): upper limit of parameter range
            num_std_dev (int): number of standard deviations to use for
                distribution. Only values within [lower, upper] limit range
                will be returned
        """
        self.name = name
        self.freqs = freqs
        self.values = values

        try:
            verify_kwargs(kwargs, Tolerance.KWARGS)  # verify sufficient kwargs
            self.tolerance = Tolerance(**kwargs)
        except ValueError:
            # if minimum kwargs are not present, don't create tolerance object
            pass

    def get_value(self, freq):
        """
        Get the value of a parameter for a particular frequency
        Args:
            freq (int): Frequency in MHz

        Returns:
            value (float): parameter value
        """
        if len(self.freqs) == 1:
            # just a single value for all freqs, so just return that value
            return self.values[0]
        else:
            if freq < min(self.freqs):
                freq = min(self.freqs)
            elif freq > max(self.freqs):
                freq = max(self.freqs)
            # interpolate value
            value = np.interp(freq, self.freqs, self.values)
            return value

    def update_value(self, freq, value):
        """
        Update a parameter or add a new one

        Args:
            freq (float): Parameter frequency in MHz
            value (float): parameter value

        Returns:
            None
        """
        if freq in self.freqs:
            # freq already exists so just update it
            idx = self.freqs.index(freq) # find index of freq
            self.values[idx] = value    # update value
        else:
            # this is a new frequency so insert the value at the correct spot
            idx = len([x for x in self.freqs if x < freq])  # find the correct index to stick the new value
            self.freqs.insert(idx, freq)
            self.values.insert(idx, value)


class Tolerance:
    TYPES = ['DB', 'PER']
    DISTS = ['UNIFORM', 'NORMAL']
    KWARGS = ['tol', 'limits']

    def __init__(self, tol, limits,
                 dist='uniform', num_std_dev=3):
        """
        Class to handle parameter tolerances
        Args:
            tol (str): type of tolerance [dB or per]
            dist (str): Distribution type (uniform, normal)
            limits (list): [lower, upper]
            num_std_dev (int): number of standard deviations to use for
                distribution. Only values within [lower, upper] limit range
                will be returned

        returns:
            value (float): parameter value
        """
        validate_arg(tol.upper(), Tolerance.TYPES)
        validate_arg(dist.upper(), Tolerance.DISTS)

        self.tol = tol.upper()
        self.limits = limits
        self.dist = dist.upper()
        self.num_dev = num_std_dev

    def get_value(self, mean=None):
        """
        Return a random value with the limits based on the defined
        distribution

        Args:
            mean(float): mean value to determine a statistical value from

        Returns:
            value (float)
        """
        value = 0
        if self.dist == 'UNIFORM':
            valid = False
            while valid is False:
                value = random.uniform(self.limits[0], self.limits[1])
                valid = self._validate_value(value)
        else:
            if mean is None:
                raise ValueError("A mean argument is required for parameters with normal tolerance distributions")
            # the stddev is the range of limit values divided by the number
            # of standard deviations we want to include in the distribution.
            # With the default value of 3, 99.7% of values will be within
            # the limit range.
            sigma = (self.limits[1] - self.limits[0]) / self.num_dev
            valid = False
            while valid is False:
                value = random.gauss(mean, sigma)
                valid = self._validate_value(value)

        return round(value, 2)

    def _validate_value(self, value):
        """
        Determine if value is within the limits

        Args:
            value:

        Returns:
            (bool)
        """
        if self.limits[0] <= value <= self.limits[1]:
            return True
        else:
            return False


class ComponentData(Component):
    def __init__(self, uid, name):
        """
        Container to hold simulation data for an individual component.  These objects will mirror the comp_list in
        the simulation engine 1 for 1.
        """
        super().__init__(uid, name)

    def update_parameter(self, name, freq, value):
        """
        Update a cascaded parameter value based on a new frequency.  This will also create the parameter if it
        doesn't already exist

        Args:
            name:
            freq:
            value:

        Returns:
        """
        if name not in self._parameters.keys():
            self.add_parameter(name, [freq], [value])
        else:
            param = self.get_parameter(name)
            param.update_value(freq, value)


