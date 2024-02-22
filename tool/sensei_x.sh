sudo /bin/launchctl unload /Library/LaunchDaemons/org.cindori.SenseiDaemon.plist
sudo /bin/launchctl unload /Library/LaunchDaemons/org.cindori.SenseiHelper.plist

sudo /usr/bin/killall -u root -9 org.cindori.SenseiHelper

sudo /bin/rm /Library/LaunchDaemons/org.cindori.SenseiDaemon.plist
sudo /bin/rm /Library/LaunchDaemons/org.cindori.SenseiHelper.plist

sudo /bin/rm /Library/PrivilegedHelperTools/org.cindori.SenseiHelper
helper='/Applications/Sensei.app/Contents/Library/LaunchServices/org.cindori.SenseiHelper'
xattr -c '/Applications/Sensei.app'
src_info='/Applications/Sensei.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:org.cindori.SenseiHelper \"identifier \\\"org.cindori.SenseiHelper\\\"\"" "$src_info"
codesign -f -s - --all-architectures --deep /Applications/Sensei.app/Contents/Library/LaunchServices/org.cindori.SenseiHelper
codesign -f -s - --all-architectures --deep /Applications/Sensei.app