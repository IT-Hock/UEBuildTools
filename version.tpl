#pragma once

#define VERSION_CHANGELIST "{{changelist}}"
#define VERSION_BRANCH "{{branch}}"
#define VERSION_VISIBILITY "{{visibility}}"
#define VERSION_SHORT "{{versionShort}}"
#define VERSION_FULL "{{version}}"
#define VERSION_TIME __DATE__ "/" __TIME__
#define VERSION_PUBLIC {{isPublic}}

#define VERSION_STRING "Version " VERSION_FULL " (" VERSION_TIME ") [" VERSION_VISIBILITY "] <" VERSION_BRANCH "/" VERSION_SHORT "> ChangeList: " VERSION_CHANGELIST
