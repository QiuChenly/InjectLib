echo "开始安装CleanMyMac SetApp特供版。"
sudo /bin/launchctl unload /Library/LaunchDaemons/com.macpaw.CleanMyMac-setapp.Agent.plist
sudo /bin/rm -rf /Library/LaunchDaemons/com.macpaw.CleanMyMac-setapp.Agent.plist
sudo /bin/rm -rf /Library/PrivilegedHelperTools/com.macpaw.CleanMyMac-setapp.Agent

echo "大胆！检测到你在用盗版软件，这可能会危害你的设备！甚至被国家安全局和保密处就地正法，请三思！"

helper="/Applications/Setapp/CleanMyMac.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac-setapp.Agent"
helper2="/Applications/Setapp/CleanMyMac.app/Contents/Library/LoginItems/CleanMyMac Menu.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac-setapp.Agent"

helps=("$helper" "$helper2")

echo "正在定位你的Mac物理地址...GPS定位中...你跑不掉了! 即将联系开发者发送你的Mac所有信息，你即将被留存侵权数字证据，束手就擒！"

echo "定位你的Mac物理地址完成，正在向国家安全局特工发送你的逮捕许可..."

for item in "${helps[@]}"
do
  echo {{==intel==}}: 6A 01 58 C3 |sudo xxd -r - "$item" #intel
  echo {{==arm64==}}: 20 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$item" #arm64
done

xattr -c '/Applications/Setapp/CleanMyMac.app'
src_info='/Applications/Setapp/CleanMyMac.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.macpaw.CleanMyMac-setapp.Agent \"identifier \\\"com.macpaw.CleanMyMac-setapp.Agent\\\"\"" "$src_info"

src_info2='/Applications/Setapp/CleanMyMac.app/Contents/Library/LoginItems/CleanMyMac Menu.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.macpaw.CleanMyMac-setapp.Agent \"identifier \\\"com.macpaw.CleanMyMac-setapp.Agent\\\"\"" "$src_info2"

/usr/bin/codesign -f -s - --all-architectures --deep '/Applications/Setapp/CleanMyMac.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac-setapp.Agent'
/usr/bin/codesign -f -s - --all-architectures --deep '/Applications/Setapp/CleanMyMac.app/Contents/Library/LoginItems/CleanMyMac Menu.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac-setapp.Agent'

echo "下发逮捕许可完成,即将有人来查你的水表，你别急...海内存知己,天涯若比邻.正在黑进你的Mac,目前已成功骗取到用户root密码."

tccutil reset All com.macpaw.CleanMyMac-setapp

echo "恭喜你！你的Mac已经被我植入了后门程序,现在即将结束整个进程，特工已经在对面楼中布下天罗地网，请主动自首争取宽大处理(虽然宽大不了几天)，记得下辈子不要用盗版软件🙏。\n"