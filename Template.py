# Loads a *.tpl file and replaces all instances of {{variable}} with the value of the variable in the script.
import logging
import re


class Template:
    """
    A class used to handle template files.

    ...

    Attributes
    ----------
    filename : str
        the path to the template file

    template : str
        the content of the template file

    variables : dict
        the variables to be replaced in the template

    Methods
    -------
    load():
        Loads the template from the file.

    set_variables(variables):
        Sets the variables to be replaced in the template.

    set_variable(variable, value):
        Sets a single variable to be replaced in the template.

    replace():
        Replaces all instances of {{variable}} in the template with the value of the variable.

    write(filename):
        Writes the replaced template to a new file.
    """
    filename = ""
    template = ""
    output = ""
    options = {}
    variables = {}

    def __init__(self, filename):
        """
        Constructs a new Template object.

        Parameters
        ----------
        filename : str
            The path to the template file.
        """
        self.filename = filename
        self.template = ""
        self.variables = {}
        self.load()

    def load(self):
        """
        Loads the template from the file.
        """
        logging.debug(f"Loading {self.filename}")
        with open(self.filename, 'r') as file:
            self.template = file.read()

    def set_variables(self, variables):
        """
        Sets the variables to be replaced in the template.

        Parameters
        ----------
        variables : dict
            The variables to be replaced in the template.
        """
        for key, value in variables.items():
            self.set_variable(key, value)

    def set_variable(self, variable, value):
        """
        Sets a single variable to be replaced in the template.

        Parameters
        ----------
        variable : str
            The variable to be replaced.

        value : str
            The value to replace the variable with.
        """
        logging.debug(f"Setting {variable} to {value}")
        self.variables[variable] = value

    def replace(self):
        """
        Replaces all instances of {{variable}} in the template with the value of the variable.
        """
        self.output = self.template
        for key, value in self.variables.items():
            logging.debug(f"Replacing {{{{{key}}}}} with {value}")
            self.output = re.sub(r'{{\s*' + key + r'\s*}}', value, self.output)

    def write(self, filename):
        """
        Writes the replaced template to a new file.

        Parameters
        ----------
        filename : str
            The path to the new file.
        """
        with open(filename, 'w') as file:
            file.write(self.output)
