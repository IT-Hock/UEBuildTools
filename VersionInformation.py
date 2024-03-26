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
from GitVersion import GitVersion


class VersionInformation(GitVersion):
    """
    A class used to represent the version information of a project.

    ...

    Attributes
    ----------
    public_branches : list
        a list of branch names that are considered public

    Methods
    -------
    is_public():
        Returns True if the current branch is public, False otherwise.

    set_public_branches(branches):
        Sets the list of public branches.

    add_public_branch(branch):
        Adds a new branch to the list of public branches.

    get_version_short():
        Returns a short version string in the format 'major.minor'.

    get_visibility():
        Returns 'PUBLIC' if the current branch is public, 'PRIVATE' otherwise.

    get_version_string():
        Returns a formatted version string with date, visibility, branch, version, and changelist information.
    """
    public_branches = ["master", "main", "releases"]

    def is_public(self):
        """
        Returns True if the current branch is public, False otherwise.

        Returns
        -------
        bool
            True if the current branch is public, False otherwise.
        """
        return self.branch.lower() in self.public_branches

    def set_public_branches(self, branches):
        """
        Sets the list of public branches.

        Parameters
        ----------
        branches : list
            The new list of public branches.
        """
        self.public_branches = branches

    def add_public_branch(self, branch):
        """
        Adds a new branch to the list of public branches.

        Parameters
        ----------
        branch : str
            The name of the new public branch.
        """
        self.public_branches.append(branch)

    def get_version_short(self):
        """
        Returns a short version string in the format 'major.minor'.

        Returns
        -------
        str
            The short version string.
        """
        return f"{self.version[0]}.{self.version[1]}"

    def get_version_long(self):
        """
        Returns a version string in the format 'major.minor.patch-build'.

        Returns
        -------
        str
            The version string.
        """
        return f"{self.version[0]}.{self.version[1]}.{self.version[2]}-{self.version[3]}"

    def get_visibility(self):
        """
        Returns 'PUBLIC' if the current branch is public, 'PRIVATE' otherwise.

        Returns
        -------
        str
            The visibility of the current branch.
        """
        return "PUBLIC" if self.is_public() else "PRIVATE"

    def get_version_string(self):
        """
        Returns a formatted version string with date, visibility, branch, version, and changelist information.

        Returns
        -------
        str
            The formatted version string.
        """
        return (f"({self.commit_date.strftime('%d %b %Y')}/{self.commit_date.strftime('%H:%M:%S')}) "
                f"[{self.get_visibility()}] <{self.branch}/{self.get_version_short()}> ChangeList: {self.short_sha}")
