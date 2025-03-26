def pluralize(name):
    """
    Pluralize a singular noun and ensure it's lowercase.
    :param name: The singular noun.
    :return: The pluralized and lowercase form of the noun.
    """
    if name.endswith("y") and name[-2] not in "aeiou":
        return (name[:-1] + "ies").lower()
    elif name.endswith(("s", "x", "z", "ch", "sh")):
        return (name + "es").lower()
    else:
        return (name + "s").lower()