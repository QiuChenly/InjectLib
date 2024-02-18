
echo "准备自动计算Helper偏移参数..."

cp ./tool/proxyman_o.sh ./tool/proxyman.sh

chmod +x ./tool/SearchParttenCode

./tool/SearchParttenCode proxyman

sh ./tool/proxyman.sh

rm ./tool/proxyman.sh