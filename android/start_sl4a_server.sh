#!/bin/sh
echo "$@" > /tmp/sl4a_server_args

adb shell am start -a com.googlecode.android_scripting.action.KILL_ALL -n com.googlecode.android_scripting/.activity.ScriptingLayerServiceLauncher
adb shell am start -a com.googlecode.android_scripting.action.LAUNCH_SERVER -n com.googlecode.android_scripting/.activity.ScriptingLayerServiceLauncher --ei com.googlecode.android_scripting.extra.USE_SERVICE_PORT 45001
adb forward tcp:99999 tcp:45001
