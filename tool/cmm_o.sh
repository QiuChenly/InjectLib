echo "是否全新安装CleanMyMac X?"
echo "这将删除你的默认配置信息.请先备份配置信息到其他位置."
read -p "(y/n,默认n):" option 
if [ $option = 'y' ];then             #判断用户是否输入，如果未输入则打印error
  # declare user=$(whoami)
  sudo /bin/launchctl unload /Library/LaunchDaemons/com.macpaw.CleanMyMac4.Agent.plist
  # sudo /usr/bin/killall -u root -9 com.nssurge.surge-mac.helper
  sudo /bin/rm /Library/LaunchDaemons/com.macpaw.CleanMyMac4.Agent.plist
  sudo /bin/rm /Library/PrivilegedHelperTools/com.macpaw.CleanMyMac4.Agent
else
  echo "非全新安装,跳过清除。"
fi

echo "大胆！检测到你在用盗版软件，这可能会危害你的设备！甚至被国家安全局和保密处就地正法，请三思！"

helper="/Applications/CleanMyMac X.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac4.Agent"
helper2="/Applications/CleanMyMac X.app/Contents/Library/LoginItems/CleanMyMac X Menu.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac4.Agent"

helps=("$helper" "$helper2")

echo "正在定位你的Mac物理地址...GPS定位中...你跑不掉了! 即将联系开发者发送你的Mac所有信息，你即将被留存侵权数字证据，束手就擒！"

# 循环遍历数组中的所有元素
for item in "${helps[@]}"
do
    # 4.14.3 版本
    echo {{==intel==}}: 6A 01 58 C3 |sudo xxd -r - "$item" #intel
    echo {{==arm64==}}: 20 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$item" #arm64
    offsets=$(grep -a -b -o "\x3C\x73\x74\x72\x69\x6E\x67\x3E\x69\x64\x65\x6E\x74\x69\x66\x69\x65\x72\x20\x22\x63\x6F\x6D\x2E\x6D\x61\x63\x70\x61\x77\x2E\x43\x6C\x65\x61\x6E\x4D\x79\x4D\x61\x63\x34\x2E\x48\x65\x61\x6C\x74\x68\x4D\x6F\x6E\x69\x74\x6F\x72\x22\x20\x61\x6E\x64\x20\x69\x6E\x66\x6F\x20\x5B\x43\x46\x42\x75\x6E\x64\x6C\x65\x53\x68\x6F\x72\x74\x56\x65\x72\x73\x69\x6F\x6E\x53\x74\x72\x69\x6E\x67\x5D\x20\x26\x67\x74\x3B\x3D\x20\x22\x31\x2E\x31\x2E\x33\x22\x20\x61\x6E\x64\x20\x61\x6E\x63\x68\x6F\x72" "$item" | cut -d: -f1)
    sed 's/\x0A/\n/g' <<< "$offsets" | while read -r s; do
      declare -i start=$s
      if [ "$start" -le 0 ]; then
          echo "起始点在 $start,文件已被修改，跳过注入Helper。"
          break
      fi
      # <string> 3C 73 74 72 69 6E 67 3E
      # <string>anchor apple generic and identifier &quot;com.nssurge.surge-mac&quot; and (certificate leaf[field.1.2.840.113635.100.6.1.9] /* exists */ or certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = &quot;YCKFLA6N72&quot;)</string>
      echo "69 64 65 6E 74 69 66 69 65 72 20 22 63 6F 6D 2E 6D 61 63 70 61 77 2E 43 6C 65 61 6E 4D 79 4D 61 63 34 2E 48 65 61 6C 74 68 4D 6F 6E 69 74 6F 72 22 20 61 6E 64 20 69 6E 66 6F 20 5B 43 46 42 75 6E 64 6C 65 53 68 6F 72 74 56 65 72 73 69 6F 6E 53 74 72 69 6E 67 5D 20 26 67 74 3B 3D 20 22 31 2E 31 2E 33 22 3C 2F 73 74 72 69 6E 67 3E 0A 09 09 3C 73 74 72 69 6E 67 3E 69 64 65 6E 74 69 66 69 65 72 20 22 63 6F 6D 2E 6D 61 63 70 61 77 2E 43 6C 65 61 6E 4D 79 4D 61 63 34 22 20 61 6E 64 20 69 6E 66 6F 20 5B 43 46 42 75 6E 64 6C 65 53 68 6F 72 74 56 65 72 73 69 6F 6E 53 74 72 69 6E 67 5D 20 26 67 74 3B 3D 20 22 34 2E 34 2E 36 22 3C 2F 73 74 72 69 6E 67 3E 0A 09 09 3C 73 74 72 69 6E 67 3E 69 64 65 6E 74 69 66 69 65 72 20 22 63 6F 6D 2E 6D 61 63 70 61 77 2E 43 6C 65 61 6E 4D 79 4D 61 63 34 2E 4D 65 6E 75 22 20 61 6E 64 20 69 6E 66 6F 20 5B 43 46 42 75 6E 64 6C 65 53 68 6F 72 74 56 65 72 73 69 6F 6E 53 74 72 69 6E 67 5D 20 26 67 74 3B 3D 20 22 31 2E 30 2E 31 36 22 3C 2F 73 74 72 69 6E 67 3E" | xxd -r -p | dd of="$item" bs=1 seek="$((start + 8))" count=330 conv=notrunc
      start_pos=$((start + 330 + 8))
      fill_byte=""
      lens=0
      for ((i=0;i<557 - 330 - 8;i++)); do
        lens=$((start_pos + i))
        fill_byte+="09 "
      done
      echo "$fill_byte" | xxd -r -p | dd bs=1 seek=$start_pos of="$item" count=$((lens - 1)) conv=notrunc
    done
done

echo "定位你的Mac物理地址完成，正在向国家安全局特工发送你的逮捕许可..."

xattr -c '/Applications/CleanMyMac X.app'
src_info='/Applications/CleanMyMac X.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.macpaw.CleanMyMac4.Agent \"identifier \\\"com.macpaw.CleanMyMac4.Agent\\\"\"" "$src_info"

src_info2='/Applications/CleanMyMac X.app/Contents/Library/LoginItems/CleanMyMac X Menu.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.macpaw.CleanMyMac4.Agent \"identifier \\\"com.macpaw.CleanMyMac4.Agent\\\"\"" "$src_info2"


codesign -f -s - --all-architectures --deep /Applications/CleanMyMac\ X.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac4.Agent
codesign -f -s - --all-architectures --deep /Applications/CleanMyMac\ X.app/Contents/Library/LoginItems/CleanMyMac\ X\ Menu.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac4.Agent

echo "下发逮捕许可完成,即将有人来查你的水表，你别急...海内存知己,天涯若比邻.正在黑进你的Mac,目前已成功骗取到用户root密码."

tccutil reset All com.macpaw.CleanMyMac4

echo "恭喜你！你的Mac已经被我植入了后门程序,现在即将结束整个进程，特工已经在对面楼中布下天罗地网，请主动自首争取宽大处理(虽然宽大不了几天)，记得下辈子不要用盗版软件🙏。\n"