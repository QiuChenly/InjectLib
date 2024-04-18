tccutil reset All codes.rambo.AirBuddy-setapp
helper="/Applications/Setapp/AirBuddy.app/Contents/Library/LaunchServices/codes.rambo.AirBuddy.Installer"
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
cp ./tool/Setapps/airbuddy_x.sh ./tool/Setapps/airbuddy.sh
chmod +x ./tool/GenShineImpactStarter
./tool/GenShineImpactStarter airbuddy
sh ./tool/Setapps/airbuddy.sh
rm ./tool/Setapps/airbuddy.sh
