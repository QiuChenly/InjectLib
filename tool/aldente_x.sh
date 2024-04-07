sudo /bin/launchctl unload /Library/LaunchDaemons/com.apphousekitchen.aldente-pro.helper.plist
sudo /usr/bin/killall -u root -9 com.apphousekitchen.aldente-pro.helper
sudo /bin/rm /Library/LaunchDaemons/com.apphousekitchen.aldente-pro.helper.plist
sudo /bin/rm /Library/PrivilegedHelperTools/com.apphousekitchen.aldente-pro.helper
helper='/Applications/AlDente.app/Contents/Library/LaunchServices/com.apphousekitchen.aldente-pro.helper'
xattr -c '/Applications/AlDente.app'
src_info='/Applications/AlDente.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.apphousekitchen.aldente-pro.helper \"identifier \\\"com.apphousekitchen.aldente-pro.helper\\\"\"" "$src_info"
codesign -f -s - --all-architectures --deep /Applications/AlDente.app/Contents/Library/LaunchServices/com.apphousekitchen.aldente-pro.helper
codesign -f -s - --all-architectures --deep /Applications/AlDente.app