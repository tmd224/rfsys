

class InvalidArgumentError(ValueError):
    pass


def validate_arg(arg, arg_list):
    """
    Function to validate an argument based on a valid list of possible values.
    Raises an exception if the argument is invalid

    Args:
        arg: user argument
        arg_list (list): list of valid arguments

    Returns:
        None
    """
    if arg not in arg_list:
        raise InvalidArgumentError("Argument ({}) is invalid.  Valid arguments"
                                   "are {}".format(arg, arg_list))


def verify_kwargs(kwargs, key_dict):
    """
    Verify that every key in key_dict exists in kwargs dict. Raises an
    exception with all missing keys

    Args:
        kwargs:
        key_dict:

    Returns:
        None
    """
    missing_keys = list()
    kwargs_keys = list(kwargs.keys())
    for key in key_dict:
        if key not in kwargs_keys:
            missing_keys.append(key)

    if len(missing_keys) > 0:
        raise InvalidArgumentError("Insufficient kwargs - missing keys: {}"
                                   .format(missing_keys))
