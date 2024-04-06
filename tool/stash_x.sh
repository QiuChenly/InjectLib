echo "是否全新安装Stash?"
echo "这将删除你的默认配置信息.请先备份配置信息到其他位置."
read -p "(y/n,默认n):" option
if [ $option = 'y' ];then             #判断用户是否输入，如果未输入则打印error
  sudo /bin/launchctl unload /Library/LaunchDaemons/ws.stash.app.mac.daemon.helper.plist
  sudo /bin/rm /Library/LaunchDaemons/ws.stash.app.mac.daemon.helper.plist
  sudo /bin/rm /Library/PrivilegedHelperTools/ws.stash.app.mac.daemon.helper
fi
sudo chmod 744 "/Applications/Stash.app/Contents/Library/LaunchServices/ws.stash.app.mac.daemon.helper"
xattr -c '/Applications/Stash.app'
src_info='/Applications/Stash.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:ws.stash.app.mac.daemon.helper \"identifier \\\"ws.stash.app.mac.daemon.helper\\\"\"" "$src_info"
codesign -f -s - --all-architectures --deep /Applications/Stash.app/Contents/Library/LaunchServices/ws.stash.app.mac.daemon.helper
codesign -f -s - --all-architectures --deep /Applications/Stash.app