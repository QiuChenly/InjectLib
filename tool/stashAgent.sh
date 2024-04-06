tccutil reset All ws.stash.app.mac
helper="/Applications/Stash.app/Contents/Library/LaunchServices/ws.stash.app.mac.daemon.helper"
backup="${helper}_backup"
if [ -e "$backup" ];
then
  echo "检测到helper备份文件存在，可能是二次注入，删除已注入的helper"
  rm "$helper"
  cp "$backup" "$helper"
else
  echo "未检测到helper备份文件，首次注入，已备份helper文件"
  cp "$helper" "$backup"
fi
echo "准备自动计算Helper偏移参数..."
cp ./tool/stash_x.sh ./tool/stash.sh
chmod +x ./tool/QAQ_GenshineImpactStarter
./tool/QAQ_GenshineImpactStarter stash
sh ./tool/stash.sh
rm ./tool/stash.sh