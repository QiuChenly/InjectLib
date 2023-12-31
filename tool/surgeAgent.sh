if [ -e "/Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper_backup" ];
then
  echo "检测到helper备份文件存在，可能是二次注入，删除已注入的helper"
  rm /Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper
  cp /Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper_backup /Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper
else
  echo "未检测到helper备份文件，首次注入，已备份helper文件"
  cp /Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper /Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper_backup
fi
echo "准备自动计算Helper偏移参数..."

cp ./tool/surge_o.sh ./tool/surge.sh

chmod +x ./tool/SearchParttenCode

./tool/SearchParttenCode surge

sh ./tool/surge.sh

rm ./tool/surge.sh