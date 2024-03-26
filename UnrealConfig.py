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
# Loads a INI File from unreal
import logging
import re


class UnrealConfig:
    """
    A class used to handle Unreal Engine configuration files.

    ...

    Attributes
    ----------
    path : str
        the path to the configuration file

    config : dict
        the configuration data loaded from the file

    Methods
    -------
    load():
        Loads the configuration data from the file.

    get(section=None, key=None):
        Returns the value for a given key in a given section. If no key is provided, returns the entire section. If no section is provided, searches all sections for the key.

    set(section, key, value):
        Sets the value for a given key in a given section.

    save():
        Saves the current configuration data back to the file.
    """
    def __init__(self, path):
        """
        Constructs a new UnrealConfig object.

        Parameters
        ----------
        path : str
            The path to the configuration file.
        """
        self.path = path
        self.config = self.load()

    def load(self):
        """
        Loads the configuration data from the file.

        Returns
        -------
        dict
            The configuration data.
        """
        with open(self.path, 'r') as f:
            lines = f.readlines()
            config = {}
            for line in lines:
                if line == '\n' or line == '' or line == '\r\n':
                    continue
                line = line.strip()
                # Regex match key=value
                if re.match(r'^.*?=.*?$', line):
                    key, value = line.split('=', 1)
                    config[section][key] = value
                # Regex match [section]
                elif re.match(r'^\[.*]$', line):
                    section = line[1:-1]
                    config[section] = {}
                else:
                    logging.error(f"Line: {line}")
                    raise Exception("Invalid INI File")
            return config

    def get(self, section=None, key=None):
        """
        Returns the value for a given key in a given section. If no key is provided, returns the entire section. If no section is provided, searches all sections for the key.

        Parameters
        ----------
        section : str, optional
            The section to search in.

        key : str, optional
            The key to search for.

        Returns
        -------
        str or dict
            The value for the key, or the entire section.
        """
        if key is None:
            return self.config[section]
        if section is None:
            for section in self.config:
                if key in self.config[section]:
                    return self.config[section][key]

        return self.config[section][key]

    def set(self, section, key, value):
        """
        Sets the value for a given key in a given section.

        Parameters
        ----------
        section : str
            The section to set the value in.

        key : str
            The key to set the value for.

        value : str
            The value to set.
        """
        self.config[section][key] = value

    def save(self):
        """
        Saves the current configuration data back to the file.
        """
        with open(self.path, 'w') as f:
            for section in self.config:
                f.write(f'[{section}]\n')
                for key, value in self.config[section].items():
                    f.write(f'{key}={value}\n')
                f.write('\n')

    def __str__(self):
        return str(self.config)

    def __repr__(self):
        return str(self.config)
