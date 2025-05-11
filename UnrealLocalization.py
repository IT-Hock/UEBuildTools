"""
    UEBuild Tools - Version Information Updater for Unreal Engine
    Copyright (C) 2024 IT-Hock

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
        if not match:
            logging.error(f"Line: {text}")
            return
        self.namespace = match.group(1)
        self.key = match.group(2)
        self.value = match.group(3)

    def __str__(self):
        """
        Returns a string representation of the localization string in the format 'NSLOCTEXT("namespace", "key", "value")'.

        Returns
        -------
        str
            The string representation of the localization string.
        """
        if self.namespace is None or self.key is None or self.value is None:
            logging.error("Localization is not set")
            return f'"{self.value}"'
        
        return f'NSLOCTEXT("{self.namespace}", "{self.key}", "{self.value}")'
