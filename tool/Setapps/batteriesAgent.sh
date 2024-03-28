tccutil reset All io.fadel.Batteries-setapp
helper="/Applications/Setapp/Batteries.app/Contents/Library/LoginItems/io.fadel.Batteries-setapp.Helper.app/Contents/MacOS/io.fadel.Batteries-setapp.Helper"
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
cp ./tool/Setapps/batteries_x.sh ./tool/Setapps/batteries.sh
chmod +x ./tool/QAQ_GenshineImpactStarter
./tool/QAQ_GenshineImpactStarter batteries
sh ./tool/Setapps/batteries.sh
rm ./tool/Setapps/batteries.sh