sudo /usr/bin/killall -u root -9 codes.rambo.AirBuddy.Installer
app='/Applications/Setapp/AirBuddy.app'
helper="$app/Contents/Library/LaunchServices/codes.rambo.AirBuddy.Installer"
xattr -cr "$app"
/usr/bin/codesign -f -s - --all-architectures --deep "$helper"
/usr/bin/codesign -f -s - --all-architectures --deep "$app"