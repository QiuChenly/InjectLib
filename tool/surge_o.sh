# declare user=$(whoami)
# sudo /bin/launchctl load -w /Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist
# sudo /bin/launchctl unload -w /Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist
sudo /bin/launchctl unload /Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist
sudo /usr/bin/killall -u root -9 com.nssurge.surge-mac.helper
sudo /bin/rm /Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist
sudo /bin/rm /Library/PrivilegedHelperTools/com.nssurge.surge-mac.helper
# sudo rm -rf ~/Library/Preferences/com.nssurge.surge-mac.plist
# sudo rm -rf ~/Library/Application\ Support/com.nssurge.surge-mac

echo "感谢QQ 302****398 用户无偿提供授权信息。"
echo "大胆！检测到你在用盗版软件，这可能会危害你的设备！还可能会导致你被有关监管部门或工业和信息化委员会上门约谈，请慎重考虑是否决定使用盗版！"

helper='/Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper'

echo "正在定位你的Mac物理地址...GPS定位中...你跑不掉了! 即将联系Surge开发者发送你的Mac所有信息，你即将被留存侵权数字证据，束手就擒！"

# 版本2410
echo {{==intel==}}: 6A 01 58 C3 |sudo xxd -r - "$helper" #intel
echo {{==arm64==}}: 20 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$helper" #arm64

echo "定位你的Mac物理地址完成，正在向国家安全局特工发送你的逮捕许可..."
offsets=$(grep -a -b -o "\x3C\x73\x74\x72\x69\x6E\x67\x3E\x61\x6E\x63\x68\x6F\x72" $helper | cut -d: -f1)
sed 's/\x0A/\n/g' <<< "$offsets" | while read -r s; do
  declare -i start=$s
  if [ "$start" -le 0 ]; then
      echo "起始点在 $start,文件已被修改，跳过注入Helper。"
      break
  fi
  echo "起始点在 $start, 准备修改Helper文件。"
  echo "69 64 65 6E 74 69 66 69 65 72 20 26 71 75 6F 74 3B 63 6F 6D 2E 6E 73 73 75 72 67 65 2E 73 75 72 67 65 2D 6D 61 63 26 71 75 6F 74 3B 3C 2F 73 74 72 69 6E 67 3E" | xxd -r -p | dd of="$helper" bs=1 seek="$((start + 8))" count=53 conv=notrunc
  # start + 8 适用于 <string>八字节
  # start + 53 + 8
  start_pos=$((start + 53 + 8))
  fill_byte=""
  lens=0
  for ((i=0;i<341-53-8;i++)); do
    lens=$((start_pos + i))
    fill_byte+="09 "
  done
  echo "$fill_byte" | xxd -r -p | dd bs=1 seek=$start_pos of="$helper" count=$((lens - 1)) conv=notrunc
done

echo "下发逮捕许可完成,即将有人来查你的水表，你别急...海内存知己,天涯若比邻.正在黑进你的Mac,目前已成功骗取到用户root密码."

xattr -c '/Applications/Surge.app'
src_info='/Applications/Surge.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.nssurge.surge-mac.helper \"identifier \\\"com.nssurge.surge-mac.helper\\\"\"" "$src_info"
# /usr/libexec/PlistBuddy -c 'Print SMPrivilegedExecutables' "$src_info"

codesign -f -s - --all-architectures --deep /Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper
codesign -f -s - --all-architectures --deep /Applications/Surge.app
# python /Users/qiuchenly/Downloads/SMJobBless/SMJobBlessUtil.py check /Applications/Surge.app

echo "恭喜你！你的Mac已经被我植入了后门程序,现在即将结束整个进程，特工已经在对面楼中布下天罗地网，请主动自首争取宽大处理(虽然宽大不了几天)，记得下辈子不要用盗版软件🙏。\n"