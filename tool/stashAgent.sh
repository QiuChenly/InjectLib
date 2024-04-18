helper="/Applications/Stash.app/Contents/Library/LaunchServices/ws.stash.app.mac.daemon.helper"
backup="${helper}_backup"
if [ -e "$backup" ]; then
  echo "检测到helper备份文件存在，可能是二次注入，删除已注入的helper"
  rm "$helper"
  cp "$backup" "$helper"
else
  echo "未检测到helper备份文件，首次注入，已备份helper文件"
  cp "$helper" "$backup"
fi
echo "准备自动计算Helper偏移参数..."

chmod +x ./tool/GenShineImpactStarter
./tool/GenShineImpactStarter "$helper"

echo "是否全新安装Stash?"
echo "这将删除你的默认配置信息.请先备份配置信息到其他位置."
read -p "(y/n,默认n):" option
if [ $option = 'y' ]; then #判断用户是否输入，如果未输入则打印error
  sudo /bin/launchctl unload /Library/LaunchDaemons/ws.stash.app.mac.daemon.helper.plist
  sudo /bin/rm /Library/LaunchDaemons/ws.stash.app.mac.daemon.helper.plist
  sudo /bin/rm /Library/PrivilegedHelperTools/ws.stash.app.mac.daemon.helper
fi
xattr -c '/Applications/Stash.app'
src_info='/Applications/Stash.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:ws.stash.app.mac.daemon.helper \"identifier \\\"ws.stash.app.mac.daemon.helper\\\"\"" "$src_info"
codesign -f -s - --all-architectures --deep /Applications/Stash.app/Contents/Library/LaunchServices/ws.stash.app.mac.daemon.helper
codesign -f -s - --all-architectures --deep /Applications/Stash.app
