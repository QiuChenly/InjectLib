sudo /bin/launchctl unload /Library/LaunchDaemons/com.proxyman.NSProxy.HelperTool.plist
sudo /usr/bin/killall -u root -9 com.nssurge.surge-mac.helper
sudo /bin/rm /Library/LaunchDaemons/com.proxyman.NSProxy.HelperTool.plist
sudo /bin/rm /Library/PrivilegedHelperTools/com.proxyman.NSProxy.HelperTool

echo "大胆！检测到你在用盗版软件，这可能会危害你的设备！甚至被国家安全局和保密处就地正法，请三思！"

helper='/Applications/Proxyman.app/Contents/Library/LaunchServices/com.proxyman.NSProxy.HelperTool'

echo "正在定位你的Mac物理地址...GPS定位中...你跑不掉了! 即将联系开发者发送你的Mac所有信息，你即将被留存侵权数字证据，束手就擒！"

echo 6c68: 6A 01 58 C3 |sudo xxd -r - "$helper" #intel
echo 1eb5c: 20 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$helper" #arm64

echo "定位你的Mac物理地址完成，正在向国家安全局特工发送你的逮捕许可..."
offsets=$(grep -a -b -o "\x3C\x73\x74\x72\x69\x6E\x67\x3E\x61\x6E\x63\x68\x6F\x72\x20\x61\x70\x70\x6C\x65\x20\x67\x65\x6E\x65\x72\x69\x63\x20\x61\x6E\x64\x20\x69\x64\x65\x6E\x74\x69\x66\x69\x65\x72\x20\x22\x63\x6F\x6D\x2E\x70\x72\x6F\x78\x79\x6D\x61\x6E\x2E\x4E\x53\x50\x72\x6F\x78\x79\x22\x20\x61\x6E\x64\x20\x28\x63\x65\x72\x74\x69\x66\x69\x63\x61\x74\x65\x20\x6C\x65\x61\x66\x5B\x66\x69\x65\x6C\x64\x2E\x31\x2E" $helper | cut -d: -f1)
sed 's/\x0A/\n/g' <<< "$offsets" | while read -r s; do
  declare -i start=$s
  if [ "$start" -le 0 ]; then
      echo "起始点在 $start,文件已被修改，跳过注入Helper。"
      break
  fi
  echo "起始点在 $start, 准备修改Helper文件。"
  echo "69 64 65 6E 74 69 66 69 65 72 20 22 63 6F 6D 2E 70 72 6F 78 79 6D 61 6E 2E 4E 53 50 72 6F 78 79 22 3C 2F 73 74 72 69 6E 67 3E" | xxd -r -p | dd of="$helper" bs=1 seek="$((start + 8))" count=42 conv=notrunc
  # start + 8 适用于 <string>八字节
  # start + 42 + 8
  start_pos=$((start + 42 + 8))
  fill_byte=""
  lens=0
  for ((i=0;i<320-42-8;i++)); do
    lens=$((start_pos + i))
    fill_byte+="09 "
  done
  echo "$fill_byte" | xxd -r -p | dd bs=1 seek=$start_pos of="$helper" count=$((lens - 1)) conv=notrunc
done

echo "下发逮捕许可完成,即将有人来查你的水表，你别急...海内存知己,天涯若比邻.正在黑进你的Mac,目前已成功骗取到用户root密码."

xattr -c '/Applications/Proxyman.app'
src_info='/Applications/Proxyman.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.proxyman.NSProxy.HelperTool \"identifier \\\"com.proxyman.NSProxy.HelperTool\\\"\"" "$src_info"

codesign -f -s - --all-architectures --deep /Applications/Proxyman.app/Contents/Library/LaunchServices/com.proxyman.NSProxy.HelperTool

echo "恭喜你！你的Mac已经被我植入了后门程序,现在即将结束整个进程，特工已经在对面楼中布下天罗地网，请主动自首争取宽大处理(虽然宽大不了几天)，记得下辈子不要用盗版软件🙏。\n"