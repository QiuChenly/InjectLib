echo "是否全新安装Mac Fans Control?"
read -p "(y/n,默认n):" option 
if [ $option = 'y' ];then             #判断用户是否输入，如果未输入则打印error
  # declare user=$(whoami)
  sudo /bin/launchctl unload /Library/LaunchDaemons/com.crystalidea.macsfancontrol.smcwrite.plist
  sudo /bin/rm /Library/LaunchDaemons/com.crystalidea.macsfancontrol.smcwrite.plist
  sudo /bin/rm /Library/PrivilegedHelperTools/com.crystalidea.macsfancontrol.smcwrite

  sudo rm -rf ~/Library/Preferences/com.crystalidea.macsfancontrol.smcwrite.plist
  sudo rm -rf ~/Library/Application\ Support/com.crystalidea.macsfancontrol.smcwrite
else
  echo "非全新安装,跳过清除。"
fi

echo "大胆！检测到你在用盗版软件，这可能会危害你的设备！甚至被国家安全局和保密处就地正法，请三思！"

helper="/Applications/Macs Fan Control.app/Contents/Library/LaunchServices/com.crystalidea.macsfancontrol.smcwrite" # 这里有空格下面“”一定要加上 否则傻b grep不会转义

echo "正在定位你的Mac物理地址...GPS定位中...你跑不掉了! 即将联系Surge开发者发送你的Mac所有信息，你即将被留存侵权数字证据，束手就擒！"

echo 9ba0: 6A 01 58 C3 |sudo xxd -r - "$helper" #intel
echo 1dc20: 20 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$helper" #arm64

echo "定位你的Mac物理地址完成，正在向国家安全局特工发送你的逮捕许可..."
offsets=$(grep -a -b -o "\x3C\x73\x74\x72\x69\x6E\x67\x3E\x69\x64\x65\x6E\x74\x69\x66\x69\x65\x72\x20\x63\x6F\x6D\x2E\x63\x72\x79\x73\x74\x61\x6C\x69\x64\x65\x61\x2E\x6D\x61\x63\x73\x66\x61\x6E\x63\x6F\x6E\x74\x72\x6F\x6C" "$helper" | cut -d: -f1)
sed 's/\x0A/\n/g' <<< "$offsets" | while read -r s; do
  declare -i start=$s
  echo "起始点在 $start,文件已被修改，跳过注入Helper。"
  if [ "$start" -le 0 ]; then
      break
  fi
  echo "69 64 65 6E 74 69 66 69 65 72 20 63 6F 6D 2E 63 72 79 73 74 61 6C 69 64 65 61 2E 6D 61 63 73 66 61 6E 63 6F 6E 74 72 6F 6C 3C 2F 73 74 72 69 6E 67 3E" | xxd -r -p | dd of="$helper" bs=1 seek="$((start + 8))" count=50 conv=notrunc
  start_pos=$((start + 50 + 8))
  fill_byte="09"

  for ((i=0;i<104-50-8;i++)); do
    pos=$((start_pos + i))
    echo "$fill_byte" | xxd -r -p | dd bs=1 seek=$pos of="$helper" count=1 conv=notrunc
  done
done

echo "下发逮捕许可完成,即将有人来查你的水表，你别急...海内存知己,天涯若比邻.正在黑进你的Mac,目前已成功骗取到用户root密码."

xattr -c '/Applications/Macs Fan Control.app'
src_info='/Applications/Macs Fan Control.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.crystalidea.macsfancontrol.smcwrite \"identifier \\\"com.crystalidea.macsfancontrol.smcwrite\\\"\"" "$src_info"
# /usr/libexec/PlistBuddy -c 'Print SMPrivilegedExecutables' "$src_info"

/usr/bin/codesign -f -s - --all-architectures --deep /Applications/Macs\ Fan\ Control.app/Contents/Library/LaunchServices/com.crystalidea.macsfancontrol.smcwrite
/usr/bin/codesign -f -s - --all-architectures --deep /Applications/Macs\ Fan\ Control.app
# python /Users/qiuchenly/Downloads/SMJobBless/SMJobBlessUtil.py check /Applications/Surge.app

echo "恭喜你！你的Mac已经被我植入了后门程序,现在即将结束整个进程，特工已经在对面楼中布下天罗地网，请主动自首争取宽大处理(虽然宽大不了几天)，记得下辈子不要用盗版软件🙏。\n"