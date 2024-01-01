
echo "准备自动计算Helper偏移参数..."

cp ./tool/cmmsetapp_o.sh ./tool/cmm.sh

chmod +x ./tool/SearchParttenCode

./tool/SearchParttenCode cmmxsetapp

sh ./tool/cmm.sh