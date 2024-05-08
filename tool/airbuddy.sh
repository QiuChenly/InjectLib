# ./tool/GenShineImpactStarter /Applications/AirBuddy.app/Contents/Library/LaunchServices/codes.rambo.AirBuddy.Installer codes.rambo.AirBuddy

# 检查文件是否存在
if [ ! -f "/Applications/AirBuddy.app/Contents/Library/LaunchServices/codes.rambo.AirBuddy.Installer_backup" ]; then
    cp "/Applications/AirBuddy.app/Contents/Library/LaunchServices/codes.rambo.AirBuddy.Installer" "/Applications/AirBuddy.app/Contents/Library/LaunchServices/codes.rambo.AirBuddy.Installer_backup"
fi

# 检查文件是否存在
if [ ! -f "/Applications/AirBuddy.app/Contents/MacOS/AirBuddy_backup" ]; then
    cp "/Applications/AirBuddy.app/Contents/MacOS/AirBuddy" "/Applications/AirBuddy.app/Contents/MacOS/AirBuddy_backup"
fi

cp tool/91QiuChenly.dylib /Applications/AirBuddy.app/Contents/MacOS/91QiuChenly.dylib

insert_dylib @executable_path/91QiuChenly.dylib /Applications/AirBuddy.app/Contents/MacOS/AirBuddy_backup /Applications/AirBuddy.app/Contents/MacOS/AirBuddy

codesign -f -s - /Applications/AirBuddy.app/Contents/Library/LaunchServices/codes.rambo.AirBuddy.Installer

codesign -f -s - /Applications/AirBuddy.app/Contents/Library/LoginItems/AirBuddyHelper.app

/usr/libexec/PlistBuddy -c 'Set :SMPrivilegedExecutables:codes.rambo.AirBuddy.Installer identifier \"codes.rambo.AirBuddy.Installer\"' '/Applications/AirBuddy.app/Contents/Info.plist'

codesign -f -s - /Applications/AirBuddy.app

xattr -cr /Applications/AirBuddy.app