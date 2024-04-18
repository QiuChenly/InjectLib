app="/Applications/Surge.app"
helper="$app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper"

chmod +x ./tool/GenShineImpactStarter

./tool/GenShineImpactStarter "$helper"

./tool/optool install -p "$app/Contents/Frameworks/91QiuChenly.dylib" -t "$helper"

sudo /bin/launchctl unload /Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist
sudo /usr/bin/killall -u root -9 com.nssurge.surge-mac.helper
sudo /bin/rm /Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist
sudo /bin/rm /Library/PrivilegedHelperTools/com.nssurge.surge-mac.helper

# 这是彻底删除Surge的配置项 相当于删除所有配置信息 所以慎用。
# sudo rm -rf ~/Library/Preferences/com.nssurge.surge-mac.plist
# sudo rm -rf ~/Library/Application\ Support/com.nssurge.surge-mac

echo "感谢路人A/B/C/D/E/F/G 反正随便来个人都行 提供信息。"
echo "大胆！检测到你在用盗版软件，这可能会危害你的设备！还可能会导致你被有关监管部门或工业和信息化委员会上门约谈，请慎重考虑是否决定使用盗版！"

xattr -c $app
src_info="$app/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.nssurge.surge-mac.helper \"identifier \\\"com.nssurge.surge-mac.helper\\\"\"" "$src_info"

/usr/bin/codesign -f -s - --all-architectures --deep "$helper"
/usr/bin/codesign -f -s - --all-architectures --deep "$app"
echo "恭喜你！你的Mac已经被我植入了后门程序,现在即将结束整个进程，特工已经在对面楼中布下天罗地网，请主动自首争取宽大处理(虽然宽大不了几天)，记得下辈子不要用盗版软件🙏。\n"
