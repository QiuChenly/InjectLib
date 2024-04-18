tccutil reset All com.macpaw.CleanMyMac-setapp
helper="/Applications/CleanMyMac.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac-setapp.Agent"
helper2="/Applications/CleanMyMac.app/Contents/Library/LoginItems/CleanMyMac Menu.app/Contents/Library/LaunchServices/com.macpaw.CleanMyMac-setapp.Agent"
helpers=("$helper" "$helper2")
for helper in "${helpers[@]}"; do
  # 拼接备份文件的路径
  backup="${helper}_backup"
  # 判断是否存在备份文件
  if [ -e "$backup" ]; then
    echo "检测到helper备份文件存在，可能是二次注入，删除已注入的helper"
    rm "$helper"
    cp "$backup" "$helper"
  else
    echo "未检测到helper备份文件，首次注入，已备份helper文件"
    cp "$helper" "$backup"
  fi
done
echo "准备自动计算Helper偏移参数..."
cp ./tool/Setapps/cmmsetapp_o.sh ./tool/Setapps/cmmsetapp.sh
chmod +x ./tool/GenShineImpactStarter
./tool/GenShineImpactStarter cmmxsetapp
sh ./tool/Setapps/cmmsetapp.sh
rm ./tool/Setapps/cmmsetapp.sh
