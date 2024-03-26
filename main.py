import argparse
import logging

from Template import Template
from UnrealConfig import UnrealConfig
from UnrealLocalization import UnrealLocalization
from VersionInformation import VersionInformation


def get_template_variables(version_information):
    date = version_information.commit_date
    time = date.strftime("%H:%M:%S")

    return {
        "changelist": version_information.short_sha,
        "branch": version_information.branch,
        "visibility": "PUBLIC" if version_information.is_public() else "PRIVATE",
        "isPublic": "1" if version_information.is_public() else "0",
        "versionShort": f"{version_information.version[0]}.{version_information.version[1]}.{version_information.version[2]}",
        "version": f"{version_information.version[0]}.{version_information.version[1]}.{version_information.version[2]}.{version_information.version[3]}",
        "time": time,
        "date": date.strftime("%d %b %Y")
    }


def modify_default_game(version_information, project_name, default_game_path="DefaultGame.ini"):
    logging.info(f"Updating Unreal Engine configuration files")
    default_game_config = UnrealConfig(default_game_path)

    unreal_localization = UnrealLocalization(
        default_game_config.get("/Script/EngineSettings.GeneralProjectSettings", "ProjectDisplayedTitle"))
    unreal_localization.value = f"{project_name} {version_information.get_version_string()}"
    default_game_config.set("/Script/EngineSettings.GeneralProjectSettings", "ProjectDisplayedTitle",
                            unreal_localization.__str__())
    default_game_config.set("/Script/EngineSettings.GeneralProjectSettings", "ProjectVersion",
                            f"{version_information.version[0]}.{version_information.version[1]}.{version_information.version[2]}")
    default_game_config.save()
    logging.info(f"Done updating Unreal Engine configuration files")


def modify_template_file(version_information, template_file="version.tpl", output_file="version.h"):
    logging.info(f"Loading template file {template_file} and replacing variables")
    template = Template(template_file)
    template.set_variables(get_template_variables(version_information))
    template.replace()
    logging.info(f"Writing version information to {output_file}")
    template.write(output_file)


def modify_crash_report_client(version_information, crash_report_client_path="CrashReportClient.ini"):
    logging.info(f"Updating Crash Report Client Version")
    crash_report_client_config = UnrealConfig(crash_report_client_path)
    crash_report_client_config.set("CrashReportClient", "CrashReportClientVersion",
                                   version_information.get_version_long())
    crash_report_client_config.save()
    logging.info(f"Done updating Crash Report Client Version")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dir', type=str, help='Git repository directory', required=True)
    parser.add_argument('--log', type=str, help='Log level', default="INFO")
    parser.add_argument('--game', type=str, help='Game name', default='Game')
    parser.add_argument('--output', type=str, help='Output file', default="version.h")
    parser.add_argument('--template', type=str, help='Template file', default="version.tpl")
    parser.add_argument('--default-game', type=str, help='DefaultGame.ini file', default=None)
    parser.add_argument('--no-update-default-game', action='store_true', help='Do not update DefaultGame.ini file')
    parser.add_argument('--crash-report-client', type=str, help='CrashReportClient.ini file',
                        default="CrashReportClient.ini")
    parser.add_argument('--no-update-crash-report-client', action='store_true',
                        help='Do not update CrashReportClient.ini file')
    args = parser.parse_args()

    logging.basicConfig(level=args.log, format='[%(asctime)s] [%(levelname)-8s] %(message)s')

    logging.info(f'Updating Version Informations for "{args.game}" using git repository in {args.dir}')

    if args.default_game is None and not args.no_update_default_game:
        args.default_game = args.dir + "/Config/DefaultGame.ini"
        logging.info(f"DefaultGame.ini file not specified, using {args.default_game}")

    logging.info(f"Git repository directory: {args.dir}")
    logging.info(f"Reading version information from git repository")
    git_version = VersionInformation(args.dir)
    logging.debug(f"SHA: {git_version.sha}")
    logging.debug(f"Short SHA: {git_version.short_sha}")

    modify_template_file(git_version, args.template, args.output)

    if not args.no_update_crash_report_client:
        modify_crash_report_client(git_version, args.crash_report_client)

    if not args.no_update_default_game:
        modify_default_game(git_version, args.game, args.default_game)

    logging.info(f"Done")
