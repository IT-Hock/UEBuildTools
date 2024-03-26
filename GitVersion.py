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
import logging
import re
import datetime
import git


class GitVersion:
    """
    A class used to represent the version information of a project using Git.

    ...

    Attributes
    ----------
    branch : str
        the current branch name

    sha : str
        the full SHA of the current commit

    short_sha : str
        the short SHA of the current commit

    version : list
        the version number as a list of integers in the format [major, minor, patch, build]

    commit_date : datetime
        the date and time of the current commit

    Methods
    -------
    get_datetime():
        Retrieves the date and time of the current commit.

    get_branch():
        Retrieves the current branch name.

    get_sha():
        Retrieves the full and short SHA of the current commit.

    get_version():
        Retrieves the version number from the latest tag.
    """
    branch = ""
    sha = ""
    short_sha = ""
    version = [0, 0, 0]
    commit_date = None

    def __init__(self, repo=None):
        """
        Constructs a new GitVersion object.

        Parameters
        ----------
        repo : str, optional
            The path to the Git repository. If not provided, uses the current directory.
        """
        self.repo = git.Repo(repo)
        self.git = self.repo.git
        self.get_datetime()
        self.get_branch()
        self.get_sha()
        self.get_version()

    def get_datetime(self):
        """
        Retrieves the date and time of the current commit.

        Returns
        -------
        datetime
            The date and time of the current commit.
        """
        out = self.git.show("-s", "--format=%ci", "HEAD")
        self.commit_date = datetime.datetime.strptime(out, "%Y-%m-%d %H:%M:%S %z")
        logging.debug(f"self.datetime: {self.commit_date}")
        return self.commit_date

    def get_branch(self):
        """
        Retrieves the current branch name.

        Returns
        -------
        str
            The current branch name.
        """
        self.branch = self.git.rev_parse("--abbrev-ref", "HEAD")
        return self.branch

    def get_sha(self):
        """
        Retrieves the full and short SHA of the current commit.

        Returns
        -------
        str
            The full SHA of the current commit.
        """
        self.sha = self.git.rev_parse("HEAD")
        self.short_sha = self.sha[:6]
        return self.sha

    def get_version(self):
        """
        Retrieves the version number from the latest tag.

        Returns
        -------
        list
            The version number as a list of integers in the format [major, minor, patch, build].
        """
        tag = self.git.describe("--tags", "--abbrev=0", "--always")
        logging.debug(f"git describe --tags --abbrev=0 --always: {tag}")
        match = re.match(r'(\d+)\.(\d+)\.(\d+)', tag)
        if match:
            self.version = [int(match.group(1)), int(match.group(2)), int(match.group(3)), 0]
        else:
            match = re.match(r'(\d+)\.(\d+)\.(\d+)-(\d+)', tag)
            if match:
                self.version = [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))]
            else:
                logging.error(f"Could not parse version from tag: {tag}")
                self.version = [0, 0, 1, 0]
        logging.debug(f"self.version: {self.version}")
        return self.version


if __name__ == "__main__":
    git_version = GitVersion('../../')
    print("Branch: " + git_version.branch)
    print("SHA: " + git_version.sha)
    print("Short SHA: " + git_version.short_sha)
    print("Version: " + '.'.join(map(str, git_version.version)))
    print("Date: " + git_version.commit_date)
