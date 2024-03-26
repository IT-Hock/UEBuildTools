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
import argparse
import json
import logging
import os
import sys

import requests


class TeamCity:
    host = None
    token = None

    def __init__(self, host, token):
        self.token = token
        self.host = host
        if self.host.endswith('/'):
            self.host = self.host[:-1]

    def get_headers(self):
        return {
            "Accept": "Application/JSON",
            "Authorization": "Bearer %s" % self.token
        }

    def query_tc_api(self, url):
        logging.debug("Querying TeamCity API: %s" % url)

        r = requests.get(self.host + url, headers=self.get_headers(), timeout=5)
        logging.debug("Received: %s" % r.text)
        if r.status_code != 200:
            return None, r.status_code
        return json.loads(r.text), 200

    def get_build_id(self, build_type, status='SUCCESS'):
        api_result, api_code = self.query_tc_api(
            "/app/rest/builds/?locator=buildType:%s,status:%s" % (build_type, status))
        builds = api_result['build']
        build = sorted(builds, key=lambda k: k['number'], reverse=True)[0]
        return build['id']

    def list_artifacts(self, project, bt):
        build_id = self.get_build_id(bt)
        api_result, api_code = self.query_tc_api("/app/rest/builds/id:%s/artifacts" % build_id)
        if 'file' not in api_result:
            logging.warning("No artifacts found for build type %s" % bt)
            return None

        artifacts = api_result['file']
        ret = []
        for a in artifacts:
            ret.append(a['name'])
        return ret

    def list_projects(self):
        api_result, api_code = self.query_tc_api("/app/rest/projects")
        if 'project' not in api_result:
            logging.warning("No projects found")
            return None

        projects = api_result['project']
        ret = []
        for p in projects:
            ret.append(p['id'])

        return ret

    def list_subprojects(self, project):
        api_result, api_code = self.query_tc_api("/app/rest/projects/id:%s" % project)
        if 'projects' not in api_result:
            logging.warning("No projects found for project %s" % project)
            return None
        projects = api_result['projects']
        if 'project' not in projects:
            logging.warning("No subprojects found for project %s" % project)
            return None
        subprojects = projects['project']

        ret = []
        for p in subprojects:
            ret.append(p['id'].split('_')[1])
        return json.dumps({'project': project, 'subprojects': ret}, sort_keys=True, indent=4, separators=(',', ': '))

    def list_build_types(self, project):
        api_result, api_code = self.query_tc_api("/app/rest/projects/id:%s" % "_".join([project]))
        if 'buildTypes' not in api_result:
            logging.warning("No build types found for project %s" % project)
            return None
        build_types = api_result['buildTypes']
        if 'buildType' not in build_types:
            logging.warning("No build types found for project %s" % project)
            return None
        build_type = build_types['buildType']

        ret = []
        for b in build_type:
            ret.append(b['id'])
        return ret

    def list_tags(self, project, bt):
        api_result, api_code = self.query_tc_api("/app/rest/builds/?locator=buildType:%s,lookupLimit:10" % bt)
        if 'build' not in api_result:
            logging.warning("No builds found for build type %s" % bt)
            return None

        builds = api_result['build']
        build_hrefs = [b['href'] for b in builds]
        ret = []
        for h in build_hrefs:
            api = self.query_tc_api(h)
            if 'tags' not in api:
                continue
            tags = api['tags']
            for t in tags['tag']:
                if len(t) == 40:
                    ret.append(t)
        return json.dumps({
            'project': project,
            'build_type': bt,
            'tags': ret},
            sort_keys=True, indent=4, separators=(',', ': '))

    def get_artifact(self, project, bt, artifact):
        build_id = self.get_build_id(bt)

        r = requests.get("/app/rest/builds/id:%s/artifacts/content/%s" % (build_id, artifact),
                         headers=self.get_headers())
        # Check if the request was successful
        if r.status_code != 200:
            raise Exception("%s: %s" % (r.reason, r.text))

        return r.content

    def check_connection(self):
        try:
            api_result, status_code = self.query_tc_api("/app/rest/server")
            if api_result is None:
                return False, status_code
            return True, 200
        except Exception as e:
            logging.error("Could not connect to TeamCity: %s" % e)
            return False, 500


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Name of TeamCity project')
    parser.add_argument('-b', '--buildtype', help='Build type')
    parser.add_argument('-t', '--tag', help='Tag (usually the commit sha)')
    parser.add_argument('-a', '--artifact', help='Artifact to retrieve')
    parser.add_argument('--token', help='TeamCity token')
    parser.add_argument('--host', help='TeamCity host')
    parser.add_argument('--log', help='Log level', default='INFO')

    args = parser.parse_args()

    logging.basicConfig(level=args.log, format='[%(asctime)s] [%(levelname)-8s] %(message)s')

    if args.token is not None:
        token = args.token
    elif os.getenv("TEAMCITY_TOKEN") is not None:
        token = os.getenv("TEAMCITY_TOKEN")
    else:
        logging.error("Must supply either through --token or set TEAMCITY_TOKEN env var.")
        sys.exit(1)

    if args.host is not None:
        host = args.host
    elif os.getenv("TEAMCITY_HOST") is not None:
        host = os.getenv("TEAMCITY_HOST")
    else:
        logging.error("Must supply either through --host or set TEAMCITY_HOST env var.")
        sys.exit(1)

    if not (token and host):
        logging.error("Must set TEAMCITY_TOKEN, TEAMCITY_HOST env vars.")
        sys.exit(1)

    teamcity = TeamCity(host, token)
    connection, code = teamcity.check_connection()
    if connection is False:
        logging.error("Could not connect to TeamCity")
        if code == 401:
            logging.error("Check your TEAMCITY_TOKEN")
        elif code == 404:
            logging.error("Check your TEAMCITY_HOST")
        else:
            logging.error("Received status code %d" % code)
        sys.exit(1)

    project = args.project
    if not project:
        logging.error("Must supply project. Possible values: ")
        available_projects = teamcity.list_projects()
        for available_project in available_projects:
            if available_project.startswith('_'):
                continue
            logging.error('\t%s' % available_project)
        if len(available_projects) == 0:
            logging.error("No projects found")

        sys.exit(1)

    build_type = args.buildtype
    if not build_type:
        logging.error("Must supply buildtype. Possible values: ")
        available_build_types = teamcity.list_build_types(project)
        for available_build_type in available_build_types:
            logging.error('\t%s' % available_build_type)
        if len(available_build_types) == 0:
            logging.error("No build types found for project %s" % project)

        sys.exit(1)

    artifact = args.artifact
    if not artifact:
        logging.error("Must supply artifact. Possible values: ")
        available_artifacts = teamcity.list_artifacts(project, build_type)
        for available_artifact in available_artifacts:
            logging.error('\t%s' % available_artifact)
        if len(available_artifacts) == 0:
            logging.error("No artifacts found for build type %s" % build_type)
        sys.exit(1)

    teamcity.get_artifact(project, build_type, artifact)
