tccutil reset All org.cindori.Sensei
helper="/Applications/Sensei.app/Contents/Library/LaunchServices/org.cindori.SenseiHelper"
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
cp ./tool/sensei_x.sh ./tool/sensei.sh
chmod +x ./tool/QAQ_GenshineImpactStarter
./tool/QAQ_GenshineImpactStarter sensei
sh ./tool/sensei.sh
rm ./tool/sensei.sh