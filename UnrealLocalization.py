# Can write to NSLOCTEXT("[/Script/EngineSettings]", "7128E1C24626155EBFD4BB8085E662B0", "VALUE")
import logging
import re


class UnrealLocalization:
    """
    A class used to handle Unreal Engine localization strings.

    ...

    Attributes
    ----------
    namespace : str
        the namespace of the localization string

    key : str
        the key of the localization string

    value : str
        the value of the localization string

    Methods
    -------
    parse(text):
        Parses the given text into namespace, key, and value.

    __str__():
        Returns a string representation of the localization string in the format 'NSLOCTEXT("namespace", "key", "value")'.
    """
    namespace = None
    key = None
    value = None

    def __init__(self, text):
        """
        Constructs a new UnrealLocalization object.

        Parameters
        ----------
        text : str
            The text to parse.
        """
        self.parse(text)

    def parse(self, text):
        """
        Parses the given text into namespace, key, and value.

        Parameters
        ----------
        text : str
            The text to parse.

        Raises
        ------
        Exception
            If the text is not a valid Unreal Engine localization string.
        """
        match = re.match(r'^NSLOCTEXT\("(\[.*])", "(.*)", "(.*)"\)$', text)
        if match:
            self.namespace = match.group(1)
            self.key = match.group(2)
            self.value = match.group(3)
        else:
            logging.error(f"Line: {text}")
            raise Exception("Invalid Localization")

    def __str__(self):
        """
        Returns a string representation of the localization string in the format 'NSLOCTEXT("namespace", "key", "value")'.

        Returns
        -------
        str
            The string representation of the localization string.
        """
        return f'NSLOCTEXT("{self.namespace}", "{self.key}", "{self.value}")'
